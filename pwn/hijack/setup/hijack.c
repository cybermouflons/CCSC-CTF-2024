// gcc -o hijack hijack.c -Wl,--rpath=./ -Wl,--dynamic-link=./ld-linux-x86-64.so.2
// patchelf was breaking stuff and main wasn't being identified....

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#define MAX_ALLOCATIONS 6
#define MAX_SIZE 0xe8
#define MAX_VIEWS 0x1
#define MAX_EDITS 0x1

size_t view_count = 0;
size_t edit_count = 0;
size_t idx = 0;
extern char **environ;

struct drone {
    char *name;
    unsigned int size;
};

struct drone drones[MAX_ALLOCATIONS]; 

void setup(){
    environ = 0;
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin, NULL, _IONBF, 0);
}

void banner(){
    printf("----------------------------------\n");
    printf("       Create a new drone!!!\n");
    printf("----------------------------------\n");
}

void menu(){       
    printf("\n1. Create drone.\n");
    printf("2. Delete drone.\n");
    printf("3. Edit drone.\n");
    printf("4. View drone.\n");
    printf("\nPlease enter an option from the main menu: ");
}

int get_int(){    
    char temp[32] = {0};
    read(0, temp, 31);
    return atoi(temp);
}

void create() {
    // check if max allocations have been reached
    if (idx >= MAX_ALLOCATIONS) {
        printf("[!] Max. allocations reached\n");
        return;
    }

    // get name size
    printf("Enter name size: ");
    int name_size = get_int();

    // check max size
    if (name_size > MAX_SIZE){     
        printf("[!] Max. allowed size exceeded.\n");
        return;
    }

    // assign memory for drone name
    drones[idx].size = (unsigned short) name_size;
    drones[idx].name = (char *) malloc(drones[idx].size);

    // get name
    printf("[+] Name (max %d chars): ", drones[idx].size);
    read(0, drones[idx].name, drones[idx].size);

    // increment idx
    idx++;
}

void delete(){
    printf("Index of drone to delete: ");
    size_t idx_del = (size_t)get_int();

    // check max size reached
    printf("Checking drone at index %zu\n", idx_del);
    if (idx_del >= idx) {
        printf("[!] Invalid index\n\n");
        return;
    }

    printf("[+] Deleting drone at index %zu\n", idx_del);

    // free memory for the drone's name
    free(drones[idx_del].name);
}

void edit() {
    // check if max edits have been reached
    if (edit_count >= MAX_EDITS) {
        printf("[!] Max. edits reached\n");
        return;
    }

    printf("Index of drone to edit: ");
    size_t idx_edit = (size_t)get_int();

    // Check if the index is valid
    if (idx_edit >= idx) {
        printf("[!] Invalid index.\n\n");
        return;
    }

    // Prompt the user for the new name and read it
    printf("Enter new name (max %d chars): ", drones[idx_edit].size);
    ssize_t bytes_read = read(STDIN_FILENO, drones[idx_edit].name, drones[idx_edit].size);
    printf("[+] Drone name updated.\n");

    // update edit count
    edit_count++;    
}

void view() {
    // check if max views have been reached
    if (view_count >= MAX_VIEWS) {
        printf("[!] Max. views reached\n");
        return;
    }
    
    printf("Index of drone to view: ");
    size_t idx_view = (size_t)get_int();

    // Check if the index is valid
    if (idx_view >= idx) {
        printf("[!] Invalid index.\n\n");
        return;
    }

    // Display the name of the drone
    printf("[+] Name of drone at index %zu: ", idx_view);
    write(1, drones[idx_view].name, drones[idx_view].size);

    // update view count
    view_count++;
}

int main(int argc, char** argv){
    setup();
    banner();
       
    while(1) {        
        menu();    
        int menu_option = get_int();
        if (menu_option < 1 || menu_option > 5){
            menu_option = 100;
        } 

        switch(menu_option){
            case 1:
                create();
                break;
            case 2:             
                delete();
                break;
            case 3:
                edit();
                break;
            case 4:
                view();
                break;
            default:
                printf("[!] Invalid input, try again!\n\n");
                break;
        } 
    }
}
