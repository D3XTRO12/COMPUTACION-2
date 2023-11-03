import argparse
import os
import sys

def calculate_even_sum(pid):
    even_sum = sum(i for i in range(2, pid + 1, 2))
    print(f"{pid} - {os.getppid()}: {even_sum}")

def main():
    parser = argparse.ArgumentParser(description="Calculate the sum of even numbers up to the PID.")
    parser.add_argument("-n", type=int, required=True, help="Number of child processes to create.")
    parser.add_argument("-v", action="store_true", help="Verbose mode.")
    args = parser.parse_args()

    if args.v:
        print("Start of execution")

    for _ in range(args.n):
        child_pid = os.fork()
        if child_pid == 0:  # Child process
            calculate_even_sum(os.getpid())
            if args.v:
                print(f"End of child process {os.getpid()}")
            sys.exit(0)
        elif child_pid < 0:
            print("Error creating child process.")
        else:
            os.wait()  # Parent process waits for the child to finish

    if args.v:
        print("End of execution")

if __name__ == "__main__":
    main()
