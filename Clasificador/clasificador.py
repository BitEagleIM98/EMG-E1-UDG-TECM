# from sklearn.neighbors import (NeighborhoodComponentsAnalysis,
# KNeighborsClassifier)
# from sklearn.datasets import load_iris
# from sklearn.model_selection import train_test_split
# from sklearn.pipeline import Pipeline
# X, y = load_iris(return_X_y=True)
# X_train, X_test, y_train, y_test = train_test_split(X, y,
# stratify=y, test_size=0.7, random_state=42)
# nca = NeighborhoodComponentsAnalysis(random_state=42)
# knn = KNeighborsClassifier(n_neighbors=3)
# nca_pipe = Pipeline([('nca', nca), ('knn', knn)])
# nca_pipe.fit(X_train, y_train)
# print(nca_pipe.score(X_test, y_test))
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
################################¡¡¡IMPORTANTE!!!############################
###############################¡WORK IN PROGRESS!############################

def knn_classifier():
    df = pd.read_csv('archivo_prueba.csv')
    print(df.info())
    print(df.describe())
    print(df.head())
    # Definir categorías basadas en cuantiles o intervalos
    df['Canal 16'] = pd.cut(df['Canal 16'], bins=3, labels=[0, 1, 2])
    X = df.drop(columns=['Canal 16'])  # Elimina la columna objetivo
    # Repetir los pasos de entrenamiento con el nuevo `y`
    y = df['Canal 16']
    # Dividir datos en entrenamiento y prueba (80% entrenamiento, 20% prueba)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)
    # Definir el modelo con k=5 vecinos
    knn = KNeighborsClassifier(n_neighbors=5)
    # Entrenar el modelo
    knn.fit(X_train, y_train)
    # Predicción en datos de prueba
    y_pred = knn.predict(X_test)
    # Calcular precisión
    accuracy = accuracy_score(y_test, y_pred)
    print(f'Precisión del modelo: {accuracy:.2f}')

if __name__ == '__main__':
    knn_classifier()
    
    