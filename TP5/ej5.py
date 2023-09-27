import os
import argparse

def child_process(pid, parent_pid):
    print(f"Soy el proceso {pid}, mi padre es {parent_pid}")

def main():
    parser = argparse.ArgumentParser(description="Generates N child processes.")
    parser.add_argument("-n", type=int, required=True, help="Number of child processes to create.")
    args = parser.parse_args()

    parent_pid = os.getpid()

    for i in range(args.n):
        pid = os.fork()
        if pid == 0:
            # Proceso hijo
            child_process(os.getpid(), parent_pid)
            os._exit(0)  # Salir del proceso hijo
        elif pid < 0:
            print("Error al crear el proceso hijo.")
        else:
            # Proceso padre
            os.wait()  # Esperar a que termine el hijo

if __name__ == "__main__":
    main()

