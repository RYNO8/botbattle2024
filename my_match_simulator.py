import json
import shutil
from signal import SIGKILL
import subprocess
import os
import itertools
import sys
import time
import random
import threading
# import ray
# ray.init()

NUM_PLAYERS = 5
PIPE_PERMISSIONS = 0o660
FILE_PERMISSIOSN = 0o664
DIRECTORY_PERMISSIONS = 0o775

SUBMISSIONS_DIR = "submissions"
LOGS_DIR = "logs"

def sourcesToDir(sources):
    assert all(source.endswith(".py") for source in sources)
    sources = [source[:-3] for source in sources]
    assert all("--" not in source for source in sources)
    return "--".join(sources)

def getCount(sources):
    dir_prefix = sourcesToDir(sources)
    return sum(x.startswith(dir_prefix) for x in os.listdir(LOGS_DIR))

def main(sources: list[str], OUTPUT_DIR: str):
    print("RUN", sources)
    shutil.rmtree(OUTPUT_DIR, ignore_errors=True)
    os.mkdir(OUTPUT_DIR)
    if len(sources) != NUM_PLAYERS:
        raise Exception(f"Total players in the match must be {NUM_PLAYERS}.")

    shutil.rmtree(f"{OUTPUT_DIR}/output", ignore_errors=True)
    os.mkdir(f"{OUTPUT_DIR}/output")
    shutil.rmtree(f"{OUTPUT_DIR}/input", ignore_errors=True)
    os.mkdir(f"{OUTPUT_DIR}/input")

    for player, source in enumerate(sources):
        shutil.rmtree(f"{OUTPUT_DIR}/submission{player}", ignore_errors=True)
        os.makedirs(f"{OUTPUT_DIR}/submission{player}/io", mode=DIRECTORY_PERMISSIONS)
        os.mkfifo(f"{OUTPUT_DIR}/submission{player}/io/to_engine.pipe", mode=PIPE_PERMISSIONS)
        os.mkfifo(f"{OUTPUT_DIR}/submission{player}/io/from_engine.pipe", mode=PIPE_PERMISSIONS)
        shutil.copy(f"{SUBMISSIONS_DIR}/{source}", f"{OUTPUT_DIR}/submission{player}/{source}")

    catalog = [{ "team_id": i } for i in range(NUM_PLAYERS)]
    with open(f"{OUTPUT_DIR}/input/catalog.json", "w") as f:
        f.write(json.dumps(catalog))

    player_pids = []
    oldcwd = os.getcwd()
    for player, source in enumerate(sources):
        os.chdir(f"{OUTPUT_DIR}/submission{player}")

        with (open("io/submission.log", "w") as f_log, 
            open("io/submission.err", "w") as f_err):
            process = subprocess.Popen(["python3", source], stdout=f_log, stderr=f_err)
        
        player_pids.append(process.pid)
        # print(f"[simulator]: started submission {player} (pid={process.pid}).")
        os.chdir(oldcwd)

    start_engine(OUTPUT_DIR)

    for pid in player_pids:
        # print(f"[simulator]: terminating submission pid {pid}.")
        os.kill(pid, SIGKILL)

    print("[simulator] simulation complete.")
    time.sleep(1)



def start_engine(OUTPUT_DIR: str):
    print("[simulator] started engine.")
    oldcwd = os.getcwd()
    os.chdir(OUTPUT_DIR)
    with open("output/engine.log", "w") as f_log, open("output/engine.err", "w") as f_err:
        process = subprocess.Popen(["python3", "-m", "risk_engine", "--print-recording-interactive"], stdout=subprocess.PIPE, stderr=f_err, text=True, universal_newlines=True, bufsize=1)

        while True:
            if process.stdout is not None:
                data = process.stdout.read(1)
                if not data:
                    break
                # print(data, end="", flush=True)
                f_log.write(data)
    
    with open("output/engine.err", "r") as f_err:
        error = f_err.read()
        if error: print(error)
    # with open("output/engine.log", "r") as f_log:
    #     for line in f_log.readlines()[-5:]:
    #         print(line, end="")

    os.chdir(oldcwd)
    print("[simulator] terminated engine.")



def autoSimOnce(submissions):
    print("FINDING RUN")
    # perms = list(itertools.permutations(submissions, 5))
    # random.shuffle(perms)
    # perms = perms[:500]
    # minCount = min(getCount(sources) for sources in perms)
    # for sources in perms:
    #     currCount = getCount(sources)
    #     # if currCount == minCount and ("defensive_v3.py" in sources or "defensive_v2.py" in sources):
    #     if currCount == minCount:
    #         OUTPUT_DIR = f"{LOGS_DIR}/{sourcesToDir(sources)}--{currCount}"
    #         main(sources, OUTPUT_DIR)
    #         break
    while True:
        sources = [random.choice(submissions) for _ in range(5)]
        if len(set(sources)) != 5: continue
        OUTPUT_DIR = f"{LOGS_DIR}/{sourcesToDir(sources)}--0"
        if os.path.exists(OUTPUT_DIR): continue
        main(sources, OUTPUT_DIR)
        return

# @ray.remote
def autoSim(submissions):
    for _ in range(1000):
        autoSimOnce(submissions)

def getResult(OUTPUT_DIR):
    """returns [1st place, 2nd place, ...]"""
    filename = f"{OUTPUT_DIR}/output/results.json"
    if not os.path.isfile(filename): return None
    with open(filename) as f:
        res = json.load(f)
        if res["result_type"] == "SUCCESS":
            return res["ranking"]
        else:
            print(round, res, "!!")
            return None

BLACKLIST = ["hack1.py", "hack2.py"]

if __name__ == "__main__":
    submissions = [s for s in os.listdir(SUBMISSIONS_DIR) if os.path.isfile(f"{SUBMISSIONS_DIR}/{s}") and s not in BLACKLIST]
    if len(submissions) < 5:
        raise Exception("require at least 5 submissions for auto sim")

    if len(sys.argv) == 1:
        autoSim(submissions)
    elif len(sys.argv) >= 2:
        targets = sys.argv[1:]
        opponents = [s for s in submissions if s not in targets]
        random.shuffle(opponents)
        sources = (targets + opponents)[:5]
        # random.shuffle(sources)
        main(sources, "custom")
        res = getResult("custom")
        if res:
            print([sources[i] for i in res])
        else:
            os.system("cat custom/output/*.err")
    else:
        raise Exception("invalid usage")
