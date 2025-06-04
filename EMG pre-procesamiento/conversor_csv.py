import lectura_datos_individuales as ld
import pandas as pd

if __name__ == "__main__":
    archivo = 'P01S001R09(Ana).dat'
    senales, estados , forma_estados , forma , estimulos, trials, freq = ld.extraer_datos(archivo)
    df,forma,datos_bipolares = ld.conversion_bipolar(senales)
    df_bipolar_filtrado=ld.filtro_pb(datos_bipolares)
    df_bipolar_filtrado.to_csv('archivo_prueba2.csv', index=False)
    dataf = pd.read_csv('archivo_prueba2.csv')
    print(df_bipolar_filtrado.info())
    print(df_bipolar_filtrado.describe())
    print(df_bipolar_filtrado.head())