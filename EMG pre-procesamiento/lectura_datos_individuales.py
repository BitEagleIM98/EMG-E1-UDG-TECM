from BCI2kReader import BCI2kReader as b2k
import numpy as np
import os
import matplotlib.pyplot as plt
import pandas as pd
import re
import Filtros.Filtro_pb as fpb 
import Filtros.Filtro_comp as fcmp
import codigos_movimientos as cm

##### Banderas iniciales
debug_f = False
senal_original = False
dir_local = True # Poner en False para ingresar directorio de la carpeta del proyecto en Git

def obtener_archivos_carpeta(carpeta):
    archivos = os.listdir(carpeta)
    archivos_interes = [i for i in archivos if i.startswith("P") and i.endswith(".dat")]
    def extraer_numero(archivo):
        relacion = re.search(r'(\d+)\.dat$',archivo)
        return int(relacion.group(1)) if relacion else float('inf')
    archivos_ordenados = sorted(archivos_interes, key=extraer_numero)
    runs = len(archivos_ordenados)
    return archivos_ordenados , runs

def extraer_datos(dir,arch):
    datoscrudos = os.path.join(dir, arch)
    print(datoscrudos)
    datos=b2k.BCI2kReader(datoscrudos)
    forma=datos.signals.shape
    senales=datos.signals
    forma_estados=datos.states.shape
    estados = datos.states
    estimulos = datos.states['StimulusCode']
    secuencia = datos.parameters['Sequence']
    secuencia_array=np.array(secuencia)
    frecuencia = int(datos.samplingrate)
    slides_trial = 4
    trials = int(len(secuencia) / slides_trial)
    #senales = np.vstack([senales, estimulos])
    if debug_f == True:
        print(senales)
        print('Señales shape: ', forma)
        print('Estimulos: ', estimulos)
        print('Estimulos shape: ',estimulos.shape)
        print('Estimulos unique: ',np.unique(estimulos))
        print('Secuencia: ', secuencia_array )
        print('Tamaño de secuencia: ', len(secuencia))
        print('Trials : ', trials)
        print('Frecuencia de muestreo: ', frecuencia)
    datos.close()
    return senales , estados, forma_estados , forma, estimulos, trials, frecuencia, secuencia_array

def convertir_data_frame(datos):
    data_frame = pd.DataFrame(datos)#Matrix n (canales) x m (muestras)
    data_frame_t = np.transpose(data_frame)
    if debug_f == True :
        print('Data frame con canales monopolares: ')
        print(data_frame_t)
    return data_frame_t

def grafica(datos, canales):
    fig, axs = plt.subplots(canales, 1, figsize=(10, 2*canales), sharex=True)
    for i in range(canales):
        axs[i].plot(datos[i])
        axs[i].set_title(f'Canal {i+1}')
    plt.xlabel('Muestras')
    plt.tight_layout()
    plt.grid(True)
    plt.show()

def conversion_bipolar(datos):
    data_frame_buffer = []
    for i in range(0, 16):
        if i % 2 == 0 or i == 0:
            data_frame_buffer.append(datos[i] - datos[i+1])
    data_conv = pd.DataFrame(data_frame_buffer)
    data_frame_nuevo = np.transpose(data_conv)
    forma = data_frame_nuevo.shape
    if debug_f == True:
        print('Data frame con canales bipolares: ')
        print(data_frame_nuevo)
        print(forma)
    return data_frame_nuevo, forma , data_conv

def Matriz_3D_run(data_frame, frecuencia, num_trials, tamano_trial, canales):
    # Calcular muestras por trial
    muestras_por_trial = tamano_trial * frecuencia
    senales = np.transpose(data_frame)
    senales = senales.values
    nombres_canales = ['Ch1', 'Ch2', 'Ch3', 'Ch4', 'Ch5', 'Ch6', 'Ch7', 'Ch8']
    # Limitar a los canales y truncar los datos si es necesario
    senales = senales[:canales, :]
    muestras_totales = senales.shape[1]
    duracion_total_muestras = 8 * 60 * frecuencia  # 8 minutos de duración en muestras
    if muestras_totales > duracion_total_muestras:
        senales = senales[:, :duracion_total_muestras]
    # Crear la matriz 3D
    data3D_run = np.zeros((num_trials, canales, muestras_por_trial), dtype=np.float32)
    for i in range(num_trials):
        start_idx = i * muestras_por_trial
        end_idx = start_idx + muestras_por_trial
        if end_idx > senales.shape[1]:
            break
        data3D_run[i, :, :] = senales[:, start_idx:end_idx]
    if debug_f == True:
        print('Forma de matriz 3D: ', data3D_run.shape)
        print('Nombre de canales: ', nombres_canales)
    return data3D_run, nombres_canales

def visualizar_trial(numero_trial, matriz, seq, nombres_canales, movimiento):
    numero_trial=numero_trial - 1
    sequencia = seq
    duracion_estimulos = 2 # segundos
    num_trials = len(sequencia)//4 # Calcula el numero de trials totales, considerando 4 estimulos por trial
    trials_estimulos = sequencia.reshape(num_trials, 4)#4 estimulos por trial
    datos_trial = matriz[numero_trial, : , :]
    estimulos = trials_estimulos[numero_trial,:]
    plt.figure(figsize=(12,6))
    for i, nombre_ch in enumerate(nombres_canales):
        plt.subplot(len(nombres_canales), 1, i +1)
        plt.plot(np.arange(datos_trial.shape[1])/freq,datos_trial[i,:])
        plt.title(f'Canal {nombre_ch}')
        plt.xlabel("Tiempo (s)")
        plt.ylabel('Amplitud (uV)')
        plt.grid(True)
        for j, esti in enumerate(estimulos):
            tiempo_estimulo = j * duracion_estimulos
            plt.axvline(x=tiempo_estimulo,color='g',linestyle='--',label=f'Estímulos: {esti}' if j== 0 else '')
    plt.suptitle(f'Datos de EMG - Trial {numero_trial+1} - estímulos: {estimulos[0]},{estimulos[1]},{estimulos[2]},{estimulos[3]} - código de movimiento: {movimiento}',fontsize=14)
    plt.tight_layout()
    plt.subplots_adjust(top=0.9)
    plt.show()

def extraer_trial(movimiento,num_trial_mov,secuencia):
    trial_contador = 0
    trial = 0
    vector_trials = []
    for i in secuencia:
        trial_contador += 1
        if trial_contador == 4:
            trial += 1
            trial_contador = 0
        if i == movimiento:
            vector_trials.append(trial+1)
    num_trial = vector_trials[num_trial_mov-1]
    if debug_f == True:
        print(f'El vector con los trials que corresponden al movimiento: {movimiento}, es: {vector_trials}')
        print('El trial que se pide analizar es el numero: ', num_trial)
    return num_trial , vector_trials

####Ejemplo de uso para funciones
if __name__ == '__main__':
    if dir_local == True:
        directorio = "C:\BCI2000\BCI2000 v3.6.beta.R7385\BCI2000.x64\data\Participantes\P0T001"
    else:
        directorio = "I:\Doctorado\Git\EMG-E1-UDG-TECM\Participantes\P0T001" 
        # Pegar aquí ruta de la carpeta con informacion del participante
    archivos , corridas = obtener_archivos_carpeta(directorio)
    if debug_f == True:
        print('Carpeta contiene: ', archivos)
        print('Corridas: ', corridas)
    run = 3 #La corrida que se desea extraer
    corrida = archivos[run - 1]
    movimiento = "H1F2" # Código de movimiento que se pretende revisar en la información segmentada
    estimulo = cm.movimiento_a_estimulo(movimiento) # Numero de estimulo (movimiento) que se desea extraer de la secuencia dada (valores del 3 al 14)
    rep = 2 # Vez o repetición en que aparece el estimulo en la secuencia
    print(f'\nDatos de participante provienen de la direccion: {directorio} de donde se va a extraer el run o corrida: {run}, con el nombre de archivo .dat: {corrida}\n')
    se , es , fo_es , fo , sti, trials, freq, seq = extraer_datos(directorio, corrida)
    data_frame_bipolar, forma, datos_bipolares = conversion_bipolar(se)
    canales_bipolares = forma[1]
    data_frame_bipolar_filtrado=fpb.filtro_pb(datos_bipolares)
    if debug_f==True and senal_original == True:
        canales = fo[0]
        frame = convertir_data_frame(se)
        grafica(frame,canales)
    if debug_f == True:
        grafica(data_frame_bipolar, forma[1])
        grafica(data_frame_bipolar_filtrado, forma[1])
        fcmp.filtro_comp(se[0])
    matriz3d, nombres_canales_bipolares = Matriz_3D_run(data_frame_bipolar_filtrado, freq, trials, 8 , canales_bipolares)
    trial, arr_trials = extraer_trial(estimulo,rep,seq)
    visualizar_trial(trial,matriz3d,seq, nombres_canales_bipolares, movimiento)