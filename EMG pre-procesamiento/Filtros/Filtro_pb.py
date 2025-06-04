import pandas as pd
import numpy as np
import sys
# caution: path[0] is reserved for script path (or '' in REPL)
sys.path.insert(1, 'I:\Doctorado\Git\EMG-E1-UDG-TECM\EMG pre-procesamiento\Filtros')
from Filtro_butterworth import butter_bandpass_filter

# Parámetros del filtro
fs = 1200         # Frecuencia de muestreo en Hz (ajusta según tu señal)
lowcut = 50.0      # Frecuencia de corte inferior en Hz
highcut = 150.0   # Frecuencia de corte superior en Hz
order = 6         # Orden del filtro (un valor entre 3 y 6 suele funcionar bien en práctica)


def filtro_pb(datos_crudos):
    channels = 8
    segundos_pre_post_secuencia = 1
    segundos_pre_post_estimulo = 2 # segundos
    muestras_excedente = int((fs)*(segundos_pre_post_estimulo+segundos_pre_post_secuencia)) # 2 segundos a retirar del pre_estimulo y post_estimulo y 1 segundo a retirar del presequence y postsequence
    emg_filtrado = []
    se_emg=datos_crudos.values
    for i in range(0,channels):
        emg_filtrado.append(butter_bandpass_filter(se_emg[i], lowcut, highcut, fs, order))
    emg_filtrado = pd.DataFrame(emg_filtrado)    
    emg_filtrado_t = np.transpose(emg_filtrado)
    emg_filtrado_t = emg_filtrado_t.iloc[muestras_excedente:,:]
    emg_filtrado_t = emg_filtrado_t.iloc[:emg_filtrado_t.shape[0]-muestras_excedente,:]
    print(emg_filtrado_t.shape)
    return emg_filtrado_t