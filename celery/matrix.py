import sys
import os
from celery import Celery
import redis
import numpy as np
import math

app = Celery('matrix', backend='redis://localhost', broker='redis://localhost')

# Define Celery tasks
@app.task
def calculate_raiz(number):
    return math.sqrt(number)

@app.task
def calculate_pot(number):
    return number ** number

@app.task
def calculate_log(number):
    return math.log10(number)

# Nueva función para calcular el det
@app.task
def calculate_determinant(matrix_list):
    matrix = np.array(matrix_list)  # Convierte la lista en una matriz NumPy
    try:
        det = np.linalg.det(matrix)
        return det
    except np.linalg.LinAlgError:
        return "La matriz no es cuadrada, no se puede calcular el det."

def process_matrix(file, calculation_function):
    with open(file, 'r') as file:
        matrix = [[float(number) for number in line.strip().split(',')] for line in file]
    
    if not es_matriz_cuadrada(matrix):
        print("La matriz no es cuadrada, no se puede calcular el det.")
        return

    result = ''
    results = []
    for row in matrix:
        for number in row:
            if calculation_function == 'raiz':
                result = calculate_raiz.delay(number)
            elif calculation_function == 'pot':
                result = calculate_pot.delay(number)
            elif calculation_function == 'log':
                result = calculate_log.delay(number)
            elif calculation_function == 'det':
                result = calculate_determinant.delay(matrix)
            results.append(result)
    
    if calculation_function == 'det':
        # En lugar de imprimir cada valor, calcula el det una vez
        determinant = calculate_determinant(np.array(matrix))
        formatted_determinant = "{:.6f}".format(determinant)
        print(f"El det de la matriz es: {formatted_determinant}")
    else:
        results = [result.get() for result in results]

        for row in matrix:
            for i, number in enumerate(row):
                formatted_number = "{:.6f}".format(results[i])  # Formatea a 6 decimales
                print(formatted_number, end=", ")
            print()

def es_matriz_cuadrada(matrix):
    # Verifica si la matriz es cuadrada (mismo número de filas y columnas)
    num_filas = len(matrix)
    if num_filas == 0:
        return False
    num_columnas = len(matrix[0])
    return all(len(fila) == num_columnas for fila in matrix)

if __name__ == "__main__":
    if len(sys.argv) != 5 or sys.argv[1] != '-f' or sys.argv[3] != '-c' or sys.argv[4] not in ['raiz', 'pot', 'log', 'det']:
        print("Usage: python3 matrix.py -f /path/to/matrix_file.txt -c calculation_function")
        sys.exit(1)

    file = sys.argv[2]
    calculation_function = sys.argv[4]

    process_matrix(file, calculation_function)
