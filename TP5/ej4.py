import os
import sys

def child_process():
    child_pid = os.getpid()
    for i in range(5):
        print(f"Soy el hijo, PID {child_pid}")
    print(f"PID {child_pid} terminando")
    sys.exit(0)

def main():
    parent_pid = os.getpid()
    child_pid = os.fork()

    if child_pid == 0:
        # Proceso hijo
        child_process()
    elif child_pid < 0:
        print("Error al crear el proceso hijo.")
    else:
        # Proceso padre
        for i in range(2):
            print(f"Soy el padre, PID {parent_pid}, mi hijo es {child_pid}")
        os.wait()  # Espera a que termine el hijo
        print(f"Mi proceso hijo, PID {child_pid}, terminó")

if __name__ == "__main__":
    main()

