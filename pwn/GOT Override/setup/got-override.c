// gcc -o got-me got-me.c -Wl,--rpath=./ -Wl,--dynamic-link=./ld-linux-x86-64.so.2 -no-pie -g

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>

// Global array for data
char data[1024];

void setup(){ 
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin, NULL, _IONBF, 0);
}

int main() {
    setup();
    char input[64];
    int index, read_index;

    while (1) {
        printf("\nGET ME\n\n1. Write data at index\n2. Read data at index\n3. Exit\nChoose an option: ");
        int option;
        scanf("%d", &option);

        switch (option) {
            case 1:
                printf("Enter 32 bytes of data: ");
                read(0, input, 32);

                printf("Enter the index to write the data to: ");
                scanf("%d", &index);

                // No bounds checking here, potential for out-of-bounds write
                for (int i = 0; i < 32; i++) {
                    data[index + i] = input[i];
                }

                printf("Data written successfully.\n");
                break;

            case 2:
                printf("Enter the index to read the data from: ");
                scanf("%d", &read_index);

                // No bounds checking here, potential for out-of-bounds read
                printf("32-bytes of Data at index %d\n", read_index);
                write(1, &data[read_index], 32);
                break;

            case 3:
                printf("Exiting...\n");
                exit(0);
                return 0;

            default:
                printf("Invalid option!\n");
                break;
        }
    }
}
