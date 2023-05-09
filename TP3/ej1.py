import argparse
import os
import subprocess

def sum_pares(pid):
    suma = 0
    for i in range(0, pid+1):
        if i % 2 == 0:
            suma += i
    return suma

def main():
    parser = argparse.ArgumentParser(description='Calcula la suma de todos los números enteros pares entre 0 y el número de PID.')
    parser.add_argument('-n', type=int, help='Número de procesos hijos a generar.')
    parser.add_argument('-v', action='store_true', help='Modo verboso.')
    args = parser.parse_args()

    if args.n:
        for i in range(args.n):
            pid = os.getpid()
            if args.v:
                print(f'Proceso hijo {i} iniciado con PID {pid}.')
            suma_p = sum_pares(pid)
            print(f'{pid} - {os.getppid()}: {suma_p}')
            if args.v:
                print(f'Proceso hijo {i} finalizado con PID {pid}.')
        os.waitpid(-1, 0)

if __name__ == '__main__':
    main()