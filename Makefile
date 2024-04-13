CC = gcc
CFLAGS = -Wall -Werror -g
PYTHONFLAGS = 

SRC = library.c
LIB = libDinamica.so
SCRIPT = main.py

all: $(LIB) python 

showRequest:
	@cat response.txt
	@echo ''

python: $(LIB)
	python3 $(SCRIPT) ./$(LIB) $(PYTHONFLAGS)

$(LIB): $(SRC)
	$(CC) $(CFLAGS) -shared -o $(LIB) $(SRC)

clean:
	rm -f *.so
