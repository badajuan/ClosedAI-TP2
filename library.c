#include <stdio.h>

int hello(){
    printf("    Hello world from c!\n");
    return 0;
}

//Recibe el nombre del archivo de donde sacar los datos y el nombre del país para el cual realizar los calculos
int calcGeany(char* requestPath, char* country){
    //Do nothing
    printf("    I  received '%s' and '%s'.\n",requestPath,country);
    return 0;
}
