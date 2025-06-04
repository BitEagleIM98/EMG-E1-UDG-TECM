import numpy as np
import matplotlib.pyplot as plt
import Filtro_butterworth as fb

debug_f = False

# Parámetros del filtro
fs = 1200         # Frecuencia de muestreo en Hz (ajusta según tu señal)
lowcut = 50.0      # Frecuencia de corte inferior en Hz
highcut = 150.0   # Frecuencia de corte superior en Hz
order = 6         # Orden del filtro (un valor entre 3 y 6 suele funcionar bien en práctica)

def filtro_comp(senal):
        # Ejemplo de señal: combinamos una componente dentro de la banda de interés y otra fuera de ella.
        t = np.linspace(0, 1, 583200)  # 1 segundo de datos
        emg_signal = senal
        if debug_f == True:
            print(emg_signal)
        # Aplicar el filtro pasabanda
        filtered_emg = fb.butter_bandpass_filter(emg_signal, lowcut, highcut, fs, order)
        # Graficar la señal original y la señal filtrada
        plt.figure(figsize=(12, 6))
        plt.subplot(2, 1, 1)
        plt.plot(t, emg_signal, label="Señal original")
        plt.title("Señal EMG original (simulada)")
        plt.xlabel("Tiempo [s]")
        plt.ylabel("Amplitud")
        plt.legend()
        plt.subplot(2, 1, 2)
        plt.plot(t, filtered_emg, label="Señal filtrada (5-100 Hz)", color='red')
        plt.title("Señal EMG filtrada por Butterworth pasabanda")
        plt.xlabel("Tiempo [s]")
        plt.ylabel("Amplitud")
        plt.legend()
        plt.tight_layout()
        plt.show()