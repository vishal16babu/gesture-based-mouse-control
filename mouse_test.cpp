
#include <dos.h>
union REGS in, out;

void detect_mouse ()
{
	in.x.ax = 0;
	int86 (0X33,&in,&out);   //invoke interrupt
	if (out.x.ax == 0)
		printf ("\nMouse Failed To Initialize");
	else
		printf ("\nMouse was Succesfully Initialized");
}

int main ()
{
	detect_mouse ();
	getch ();
	return 0;
}
