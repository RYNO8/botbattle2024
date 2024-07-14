from wasmtime import Store, Module, Instance, Func, FuncType
import time

store = Store()
module = Module(store.engine, """
  (module
    (func $hello (import "" "hello"))
    (func (export "run") (call $hello))
  )
""")

R = range(100)
R2 = range(1, 200, 2)
R3 = list(range(3, 1302, 10))

def say_hello():
    x = 0
    for i in range(100000001):
       x ^= i
    print(x)

hello = Func(store, FuncType([], []), say_hello)

instance = Instance(store, module, [hello])
run = instance.exports(store)["run"]

s = time.perf_counter()
#  run(store)
say_hello()
e = time.perf_counter()
print((e - s))
