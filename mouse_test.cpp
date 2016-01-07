#include <linux/input.h>
#include <fcntl.h>
#include <stdio.h>
 #include <unistd.h>
int main(int argc, char **argv)
{
while(1) {
int fd;
if ((fd = open("/dev/input/mice", O_RDONLY)) < 0) {
   // perror("evdev open");
    //exit(1);
}

struct input_event ev;


    read(fd, &ev, sizeof(struct input_event));
    printf("value %d, type %d, code %d\n",ev.value,ev.type,ev.code);
}

return 0;
}
