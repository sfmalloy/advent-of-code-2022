CC = gcc
LDFLAGS = -no-pie -m64

all: driver

d02.o: d02.s

driver.o: driver.c

driver: driver.o d02.o

.PHONY: clean

clean:
	$(RM) *.o d02
