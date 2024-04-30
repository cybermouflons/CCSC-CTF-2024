#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <unistd.h>

//gcc -o license license.c -g

void get_flag() {
    FILE *file = fopen("flag.txt", "r");
    if (file != NULL) {
        char line[256];
        while (fgets(line, sizeof(line), file)) {
            printf("%s", line);
        }
        fclose(file);
    } else {
        printf("Error: Unable to open flag file.\n");
    }
}

bool isValidProductKey(char *productKey) {
    // Check the first 3 characters
    char *invalidPrefixes[] = {"333", "444", "555", "666", "777", "888", "999"};
    for (int i = 0; i < 7; i++) {
        if (strncmp(productKey, invalidPrefixes[i], 3) == 0) {
            return false;
        }
    }

    // Check the fourth character
    if (productKey[3] != '_') {
        return false;
    }

    // Check the last 7 characters
    char *lastSevenDigits = productKey + 4; // Skip the first 4 characters
    for (int i = 0; i < 7; i++) {
        if (lastSevenDigits[i] < '0' || lastSevenDigits[i] > '8') {
            return false;
        }
    }

    // Calculate the sum of the last 7 digits
    int sum = 0;
    for (int i = 0; i < 7; i++) {
        sum += (lastSevenDigits[i] - '0');
    }

    // Check if the sum is divisible by 7
    if (sum % 7 != 0) {
        return false;
    }

    // If all checks pass, the product key is valid
    return true;
}

bool check_password() {
    char password[16] = "OrionProtc0l!!!";
    char user_input[32];

    printf("Enter password: ");
    read(0, user_input, 32);

    if (strcmp(user_input, password) == 0) {
        return true;
    } else {
        return false;
    }
}

int main() {
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin, NULL, _IONBF, 0);

    char productKey[12] = {0};
    printf("Enter a Windows 95 product key: ");
    read(0, productKey, 12);
    productKey[12] = '\0';

    if (isValidProductKey(productKey)) {
        printf("Product key is valid!\n");
        if (check_password()) {
            printf("Password correct!\n");
            get_flag();
        } else {
            printf("Incorrect password.\n");
        }
    } else {
        printf("Invalid product key.\n");
    }

    return 0;
}
