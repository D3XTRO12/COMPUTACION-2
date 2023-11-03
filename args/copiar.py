import argparse
import os

parser = argparse.ArgumentParser(description='Copiar contenido de un archivo a otro.')
parser.add_argument('-i', '--input', type=str, required=True, help='Nombre del archivo de entrada.')
parser.add_argument('-o', '--output', type=str, required=True, help='Nombre del archivo de salida.')

args = parser.parse_args()

if not os.path.isfile(args.input):
    print(f'Error: el archivo {args.input} no existe.')
    exit()

with open(args.input, 'r') as f_input:
    content = f_input.read()

with open(args.output, 'w') as f_output:
    f_output.write(content)

print(f'Archivo {args.input} copiado a {args.output}.')



