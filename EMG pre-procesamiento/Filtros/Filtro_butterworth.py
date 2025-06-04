from scipy.signal import butter, filtfilt

def butter_bandpass(lowcut, highcut, fs, order=6):
    """
    Diseña los coeficientes de un filtro Butterworth pasabanda.
    """
    nyq = 0.5 * fs  # Frecuencia de Nyquist
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a

def butter_bandpass_filter(data, lowcut, highcut, fs, order=6):
    """
    Aplica el filtro Butterworth pasabanda a los datos usando filtfilt para evitar desfase.
    """
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = filtfilt(b, a, data)
    return y