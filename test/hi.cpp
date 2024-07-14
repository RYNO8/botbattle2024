#include "emscripten.h"
#include <cstdlib>

EMSCRIPTEN_KEEPALIVE
int f(int argc, int arr[]) {
    // int x = 0;
    // for (int i = 0; i < argc; ++i) x ^= i;
    return argc + 69;
}

EMSCRIPTEN_KEEPALIVE
int g() {
    return rand();
}

int main() {}
