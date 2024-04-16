section .text
global fTi

fTi:
    ; Proceso de conversión de float a int
    cvtss2si eax, xmm0         ; Convierte el número de punto flotante a entero y lo guarda en eax

    ; Proceso de suma
    add eax, 1                 ; Suma 1 al entero

    ; Retorno del resultado
    ret
