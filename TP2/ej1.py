import subprocess
import os
import datetime

def main():
    # Parse command line arguments
    args = parse_args()

    # Create output and log files if they don't exist
    create_file(args.output_file)
    create_file(args.log_file)

    # Execute command and write output to file
    process = subprocess.Popen(args.command.split(), stdout=subprocess.PIPE)
    output = process.communicate()[0]
    with open(args.output_file, 'a') as f:
        f.write(output.decode())

    # Write log message to file
    if process.returncode == 0:
        message = f'{datetime.datetime.now()}: Comando {args.command} ejecutado correctamente\n'
    else:
        message = f'{datetime.datetime.now()}: {output.decode()}'
    with open(args.log_file, 'a') as f:
        f.write(message)

def parse_args():
    import argparse

    parser = argparse.ArgumentParser(description='Ejecuta un comando y guarda su salida en un archivo.')
    parser.add_argument('-c', '--command', required=True, help='Comando a ejecutar')
    parser.add_argument('-f', '--output-file', required=True, help='Archivo donde se guardará la salida del comando')
    parser.add_argument('-l', '--log-file', required=True, help='Archivo donde se guardará el mensaje de log')
    return parser.parse_args()

def create_file(filename):
    if not os.path.exists(filename):
        with open(filename, 'w') as f:
            pass

if __name__ == '__main__':
    main()