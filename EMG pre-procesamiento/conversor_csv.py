import lectura_datos_individuales as ld
import Filtros.Filtro_pb as fpb
import pandas as pd

dir_local = True
debug_f = True
comp = False

if __name__ == "__main__":
    if dir_local == True:
        directorio = "C:\BCI2000\BCI2000 v3.6.beta.R7385\BCI2000.x64\data\Participantes\P0T001"
    else:
        directorio = "I:\Doctorado\Git\EMG-E1-UDG-TECM\Participantes\P0T001" 
        # Pegar aquí ruta de la carpeta con informacion del participante
    archivos , corridas = ld.obtener_archivos_carpeta(directorio)
    if debug_f == True:
        print('Carpeta contiene: ', archivos)
        print('Corridas: ', corridas)
        run = 3 #La corrida que se desea extraer
    corrida = archivos[run - 1]
    senales, estados , forma_estados , forma , estimulos, trials, freq, secuencia = ld.extraer_datos(directorio,corrida)
    df,forma,datos_bipolares = ld.conversion_bipolar(senales)
    df_bipolar_filtrado=fpb.filtro_pb(datos_bipolares)
    df_bipolar_filtrado.to_csv('archivo_prueba.csv', index=False)
    if comp == True:
        print('Comprobando la lectura del archivo csv...')
        dataf = pd.read_csv('archivo_prueba.csv')
        print(dataf.info())
        print(dataf.describe())
        print(dataf.head())
        print('Archivo csv leído correctamente')