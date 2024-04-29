#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

char cmd[16]; // Global variable

int main() {
    setbuf(stdout, NULL);

    char local_var[16]; // Local variable with size 16

    // Print current date
    system("date");

    puts("Reading 16 bytes into global variable cmd:");
    read(STDIN_FILENO, cmd, 16);

    puts("Reading 64 bytes into local variable local_var:");
    read(STDIN_FILENO, local_var, 64);

    return 0;
}
