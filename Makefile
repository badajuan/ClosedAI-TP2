CC = gcc
CFLAGS = -Wall -Werror -g
PYTHONFLAGS = 

ASM = floatToInt
SRC = library.c
LIB = libDinamica.so
SCRIPT = main.py

all: assembler $(LIB) python 

showRequest:
	@cat response.txt
	@echo ''

assembler: 
	nasm -f elf64 $(ASM).asm -o $(ASM).o

python: $(LIB)
	python3 $(SCRIPT) ./$(LIB) $(PYTHONFLAGS)

$(LIB): $(SRC) $(ASM).o
	$(CC) $(CFLAGS) -shared -o $(LIB) $(SRC) $(ASM).o

clean:
	rm -f *.so *.o