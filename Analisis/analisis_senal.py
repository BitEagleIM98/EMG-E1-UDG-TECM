import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
################################# Work in progress #########################
dir_local = True
comprobacion = True

if __name__ == '__main__':
    datos = pd.read_csv('archivo_prueba.csv')
    if comprobacion == True:
        print(datos)
        print(datos.info())
        print(datos.describe())
        print(datos.head())