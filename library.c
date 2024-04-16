#include <stdio.h>
extern int fTi(float numero);
//Recibe un flotante y redondea al entero mas cercano
int floatToInt(float value){
    int resultado = fTi(value);
    return resultado;
}
