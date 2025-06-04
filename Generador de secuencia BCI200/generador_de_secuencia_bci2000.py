import random


def generador_de_secuencia(n,m):
    arr=[]
    numeros_generados = []
    contador = {i: 0 for i in range(3, 15)}
    while any(v < n for v in contador.values()):
        # Generar un número aleatorio entre 3 y 14
        num = random.randint(3, m+2)
        # Verificar si el número no ha alcanzado su límite de repeticiones
        if contador[num] < n:
            contador[num] += 1
            numeros_generados.append(str(num))
    arr.append(str(len(numeros_generados)*4))
    for j in numeros_generados:
        arr.append(str(2))
        arr.append(str(1))
        arr.append(j)
        arr.append(str(15))
    secuencia_generada=' '.join(arr)
    print(len(numeros_generados))
    return secuencia_generada

def cantidad_muestras_aprox_totales(segundos, movimientos, repeticiones, muestreo_por_segundo):
    cantidad_muestras=segundos*movimientos*repeticiones*muestreo_por_segundo
    return cantidad_muestras

def cantidad_muestras_aprox_por_trial(segundos, muestreo_por_segundo):
    cantidad_muestras=segundos*muestreo_por_segundo
    return cantidad_muestras

if __name__ == '__main__':
    cantidad_repeticiones = 5
    cantidad_movimientos = 12
    cantidad_segundos_por_trial = 8
    sample_rate = 1000
    cadena_secuencia_final=generador_de_secuencia(cantidad_repeticiones,   cantidad_movimientos)
    muestras = cantidad_muestras_aprox_totales(cantidad_segundos_por_trial,cantidad_movimientos,cantidad_repeticiones, sample_rate)
    muestras_trial = cantidad_muestras_aprox_por_trial(cantidad_segundos_por_trial, sample_rate)
    print(cadena_secuencia_final)
    print('El tamaño final de muestras por la corrida (run) debe de ser aproximado a: ', muestras , ' muestras')
    print('La cantidad de muestras entre cada trial de: ', cantidad_segundos_por_trial , ' segundos es: ',muestras_trial)