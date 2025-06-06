from BCI2kReader import BCI2kReader as b2k
import numpy as np
import os
import lectura_datos_individuales as ldi
import Filtros.Filtro_pb as fpb
import matplotlib.pyplot as plt

debug_f = False
visual_f = False
bipolar_ch_f = True # Para convertir en canales bipolares y filtrar, siempre mantener en True

fs = 1200 # Frecuencia de muestreo

def extraer_datos_completos(directorio, archivos):
    canales = 16
    nombres_ch = None 
    for indice, nombre_arch in enumerate(archivos):
        path = os.path.join(directorio, nombre_arch)
        print(f'Procesando archivo {indice+1}/{len(archivos)}: {nombre_arch}')
        try:
            with b2k.BCI2kReader(path) as data:
                senales, estados = data.readall()
                if nombres_ch is None:
                    nombres_ch = data.parameters['ChannelNames'][:canales]
            senales = senales[:canales, :]
        except Exception as e:
            print(f'Error al procesar el archivo {nombre_arch}: {str(e)}')
    return senales

def datos_preproc(datos):
    data_frame_bipolar, forma, datos_bipolares=ldi.conversion_bipolar(datos)
    data_frame_bipolar_filtrado=fpb.filtro_pb(datos_bipolares)
    data_frame_bipolar_filtrado = np.transpose(data_frame_bipolar_filtrado)
    datos_bipolares_filtrados=data_frame_bipolar_filtrado.values
    return datos_bipolares_filtrados

def Matriz3D_completa(dir, lista):
    tamano_trial = 8
    muestras_por_trial = tamano_trial * fs
    datos = []
    indices_archivos = {}
    trial_actual_indice = 0
    nombres_ch = None
    trials = 60
    trials_y = 0
    y = []  

    for indice, nombre_arch in enumerate(lista):
        canales = 16
        path = os.path.join(dir, nombre_arch)
        print(f'Procesando archivo {indice+1}/{len(lista)}: {nombre_arch}')
        try:
            with b2k.BCI2kReader(path) as data:
                senales, estados = data.readall()
                if nombres_ch is None:
                    nombres_ch = data.parameters['ChannelNames'][:canales]
            senales = senales[:canales, :]
            muestras_totales = senales.shape[1]
            duracion_total_muestras = 8*60*fs
            if bipolar_ch_f == True:
                senales=datos_preproc(senales) #Conversion de canales bipolares, recorte de muestra para que coincida con marcas del trial y filtro pasabanda
                canales = 8

            if muestras_totales > duracion_total_muestras:
                senales = senales[:,:duracion_total_muestras]
            
            max_trials = senales.shape[1]//muestras_por_trial
            ac_trials = min(trials, max_trials)

            datos_archivo = np.zeros((ac_trials,canales,muestras_por_trial),dtype=np.float32)
            indice_init_matriz = trial_actual_indice

            for i in range(ac_trials):
                start_idx = i * muestras_por_trial
                end_idx = start_idx + muestras_por_trial
                if debug_f == True:
                    print('Vuelta: ',i)

                if end_idx <= senales.shape[1]:
                    datos_archivo[i,:,:] = senales[:,start_idx:end_idx]
                y.append(trials_y+1)
                trials_y += 1
            
            datos.append(datos_archivo)

            indice_fin_matriz = indice_init_matriz + ac_trials
            indices_archivos[nombre_arch] = (indice_init_matriz, indice_fin_matriz)
            trial_actual_indice = indice_fin_matriz
        
        except Exception as e:
            print(f'Error al procesar el archivo {nombre_arch}: {str(e)}')
    trials_totales = sum(dat.shape[0] for dat in datos)
    datos3D_participante = np.zeros((trials_totales,canales,muestras_por_trial),dtype=np.float32)
    indice_trial = 0
    for file_data in datos:
        num_file_trials = file_data.shape[0]
        datos3D_participante[indice_trial:indice_trial+num_file_trials]=datos_archivo
        indice_trial += num_file_trials
    return datos3D_participante, nombres_ch,indices_archivos, y

def visualizar_EMG_participamte(datamatrix, channel_names):
    trial_length=8
    # Obtener dimensiones
    num_trials, num_channels, samples_per_trial = datamatrix.shape 
    # Crear vector de tiempo para cada trial
    tiempo = np.linspace(0, trial_length, samples_per_trial)
    # 1. Visualización de todos los canales y todos los trials simultáneamente
    def plot_all_channels_all_trials():
        # Definir colores para cada trial
        colores = plt.cm.jet(np.linspace(0, 1, num_trials))
        # Crear figura grande 
        fig = plt.figure(figsize=(18, 3 * num_channels))
        # Calcular el escalado para mejor visualización
        # Tomar el percentil 99 para evitar que valores extremos afecten la escala
        max_val = np.percentile(np.abs(datamatrix), 99)
        y_offset = 2 * max_val  # Espaciado entre canales
        for i in range(num_channels):
            ax = fig.add_subplot(num_channels, 1, i+1)
            for j in range(num_trials):
                ax.plot(tiempo, datamatrix[j, i, :], color=colores[j], alpha=0.7, 
                        linewidth=0.8, label=f'Trial {j+1}' if i == 0 else "")
            # Añadir líneas de tiempo cada 5 segundos
            for t in range(0, int(trial_length) + 1, 5):
                if t > 0 and t < trial_length:
                    ax.axvline(x=t, color='gray', linestyle='--', alpha=0.5)  
            ax.set_title(f'Canal: {channel_names[i]}')
            ax.set_ylabel('Amplitud (μV)')
            ax.set_xlim(0, trial_length)
            # Solo mostrar etiqueta de eje x en el último subplot
            if i == num_channels - 1:
                ax.set_xlabel('Tiempo (s)')
            # Mostrar las marcas de tiempo
            ax.set_xticks(np.arange(0, trial_length + 1, 5))
            if i == 0:
                # Añadir leyenda solo al primer subplot
                ax.legend(loc='upper right', bbox_to_anchor=(1.15, 1), ncol=min(num_trials, 5))
        # Ajustar espacio entre subplots
        plt.tight_layout()
        plt.show()

    # 2. Visualización de todos los trials para un canal específico
    def plot_all_trials_single_channel(canal_idx=0):
        plt.figure(figsize=(15, 8))
        for i in range(num_trials):
            plt.plot(tiempo, datamatrix[i, canal_idx, :], alpha=0.5, label=f'Trial {i+1}')
        plt.title(f'Todos los trials para el canal {channel_names[canal_idx]}')
        plt.xlabel('Tiempo (s)')
        plt.ylabel('Amplitud (μV)')
        plt.grid(True, alpha=0.3)
        plt.legend(loc='upper right', bbox_to_anchor=(1.15, 1), ncol=2)
        plt.tight_layout()
        plt.show()
    # 3. Visualización de un trial específico con segmentación cada 5 segundos
    def plot_single_trial_segmented(trial_idx=0):
        # Crear una única figura para los canales EMG sin espacio para los botones
        fig_emg = plt.figure(figsize=(18, 2.5 * num_channels))
        # Definir colores para las áreas sombreadas
        segment_colors = ['#f0f9e8', '#bae4bc', '#7bccc4', '#43a2ca', '#0868ac']
        # Calcular el número de segmentos de 5 segundos
        num_segments = int(np.ceil(trial_length / 5))
        if num_segments > len(segment_colors):
            segment_colors = plt.cm.viridis(np.linspace(0, 0.8, num_segments))
        # Crear subplots con espacio optimizado
        axes = fig_emg.subplots(num_channels, 1, sharex=True)
        # Asegurarse de que axes sea siempre una lista para iterar sobre ella
        if num_channels == 1:
            axes = [axes]
        for i, ax in enumerate(axes):
            # Dibujar el EMG completo del trial seleccionado
            ax.plot(tiempo, datamatrix[trial_idx, i, :], 'k-', linewidth=1.2, label=f'Trial {trial_idx+1}')
            # Añadir áreas sombreadas para cada segmento de 5 segundos como referencia visual
            for seg in range(num_segments):
                start_time = seg * 5
                end_time = min((seg + 1) * 5, trial_length)  
                # Añadir área sombreada para el segmento
                ax.axvspan(start_time, end_time, 
                          alpha=0.15, 
                          color=segment_colors[seg % len(segment_colors)],
                          label=f'Segmento {seg+1}' if i == 0 else "") 
                # Añadir línea vertical al inicio de cada segmento
                ax.axvline(x=start_time, color='gray', linestyle='--', alpha=0.7)
                # Añadir etiqueta del segmento más compacta
                y_pos = ax.get_ylim()[1] * 0.85
                ax.text(start_time + 2.5, y_pos, f"Seg {seg+1}", 
                       fontsize=9, ha='center', 
                       bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="gray", alpha=0.7))
            # Añadir línea final
            ax.axvline(x=trial_length, color='gray', linestyle='--', alpha=0.7)
            # Configurar subplot
            ax.set_title(f'Canal: {channel_names[i]} - Trial {trial_idx+1}', fontsize=11)
            ax.set_ylabel('Amplitud (μV)')
            # Ajustar márgenes de los subplots
            ax.margins(x=0.01, y=0.1)
            # Solo mostrar etiqueta de eje x en el último subplot
            if i == num_channels - 1:
                ax.set_xlabel('Tiempo (s)')
            # Mostrar las marcas de tiempo cada 5 segundos
            ax.set_xticks(np.arange(0, trial_length + 1, 5))
        # Ajustar el título principal
        plt.suptitle(f'Trial {trial_idx+1} con marcadores cada 5 segundos', fontsize=14, y=0.98)
        # Ajuste fino de márgenes para eliminar espacio en blanco
        plt.subplots_adjust(left=0.05, right=0.98, top=0.95, bottom=0.1, hspace=0.3)
        # Mostrar la gráfica sin botones de segmento
        plt.show()
        
    # Mostrar información básica sobre los datos
    print(f"\nDatos EMG cargados:")
    print(f"  - Número de trials: {num_trials}")
    print(f"  - Número de canales: {num_channels}")
    print(f"  - Muestras por trial: {samples_per_trial}")
    print(f"  - Duración del trial: {trial_length} segundos")
    print(f"  - Frecuencia de muestreo: {fs} Hz")
    
    # Retornar diccionario con todas las funciones de visualización
    return {
        "plot_all_channels_all_trials": plot_all_channels_all_trials,
        "plot_all_trials_single_channel": plot_all_trials_single_channel,
        "plot_single_trial_segmented": plot_single_trial_segmented,
    }

####Ejemplo de uso para funciones
if __name__ == '__main__':
    #### remplazar por directorio con datos del participante
    #directorio = "C:\BCI2000\BCI2000 v3.6.beta.R7385\BCI2000.x64\data\Participantes\P0T001"
    directorio = "I:\Doctorado\Git\EMG-E1-UDG-TECM\Participantes\P0T001" # Pegar aquí ruta de la carpeta con informacion del participante
    archivos , corridas = ldi.obtener_archivos_carpeta(directorio)
    n_trial= 5 #Número de trial que se quiere visualizar 1 - 540
    n_channel=1 #Número de canal que se quiere visualizar 1 - 8
    #Operaciones para hacer coincidir el número ingresado con el index
    n_trial= n_trial-1 
    n_channel=n_channel-1
    matriz3d_completa, nombres_canales_matriz3d, indices_archivos, y = Matriz3D_completa(directorio, archivos)
    if debug_f == True:
        print(matriz3d_completa.shape)
    if visual_f == True:
        if debug_f == True:
            print(f"Forma de la matriz resultante: {matriz3d_completa.shape}")
            print(f"Canales: {nombres_canales_matriz3d}")
            print("Índices de cada archivo en la matriz:")
        for archivo, (inicio, fin) in indices_archivos.items():
            print(f"  {archivo}: trials {inicio} a {fin-1}")
        # Llamar a la función principal
        visualizer = visualizar_EMG_participamte(matriz3d_completa, nombres_canales_matriz3d)
        # Para ver todos los canales y trials
        visualizer["plot_all_channels_all_trials"]()
        #Para ver todos los trials en una canal especifico
        visualizer["plot_all_trials_single_channel"](n_channel) 
