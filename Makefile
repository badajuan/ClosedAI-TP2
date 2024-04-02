CC = gcc
CFLAGS = -Wall -Werror -fpic

SRC = hello.c
LIB = libhello.so
SCRIPT = main.py

all: $(LIB) python showRequest

showRequest:
	@cat response.txt
	@echo ''

python: $(LIB)
	python3 $(SCRIPT) ./$(LIB)

$(LIB): $(SRC)
	$(CC) $(CFLAGS) -shared -o $@ $<

clean:
	rm -f *.so

.PHONY: all clean
