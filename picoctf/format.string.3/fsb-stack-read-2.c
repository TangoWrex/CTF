// Code from theflash2k.me 
// Learning about format string bugs 


// gcc -o fsb-stack-read-2 fsb-stack-read-2.c -w

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define SIZE 0x50

int main() {

    char buffer[SIZE];
    char name[SIZE];
    char secret[SIZE] = { 0 };

    /* read secret from a file. */
    FILE *f = fopen("secret.txt", "r");
    fgets(secret, SIZE, f);

    printf("What is your name? ");
    fgets(name, SIZE, stdin);

    printf("Welcome ");
    printf(name);

    printf("In order to enter, you must know the admin password: ");
    fgets(buffer, SIZE, stdin);

    if(strcmp(secret, buffer) == 0) {
        puts("Welcome to the secret portion...");
        return 0;
    }
    puts("You failed!");

    return 1;
}

