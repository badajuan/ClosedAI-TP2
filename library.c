#include <stdio.h>

//Recibe un flotante y redondea al entero mas cercano
int floatToInt(float value){
    float residual = value - (int)value;
    if(residual>=0.5){
        return (int)(value+1);
    } else{
        return (int)(value);
    }
}
