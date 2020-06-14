all: align.c
	gcc -O3 -Wall -Wextra -shared align.c -o libalign.so
clean:
	$(RM) libalign.so
