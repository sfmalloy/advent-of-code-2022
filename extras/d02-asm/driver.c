#include <unistd.h>
#include <time.h>
#include <stdio.h>

extern void solve();

int main() {
    struct timespec begin, end;
    clock_gettime(CLOCK_MONOTONIC, &begin);
    solve();
    clock_gettime(CLOCK_MONOTONIC, &end);

    printf("%.3f μs\n", 1e6 * ((end.tv_sec - begin.tv_sec) + (end.tv_nsec - begin.tv_nsec) / 1e9f));
    return 0;
}
