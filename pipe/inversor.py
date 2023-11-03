import argparse
import os
import sys

def reverse_line(line, pipe_out):
    reversed_line = line[::-1]
    os.write(pipe_out, reversed_line.encode())

def main():
    parser = argparse.ArgumentParser(description="Reverse the lines of a text file.")
    parser.add_argument("-f", required=True, help="Input text file.")
    args = parser.parse_args()

    if not os.path.isfile(args.f):
        print(f"Error: The file '{args.f}' does not exist.")
        sys.exit(1)

    with open(args.f, 'r') as file:
        lines = file.readlines()

    child_processes = []

    for line in lines:
        parent_pipe_in, child_pipe_out = os.pipe()
        child_pipe_in, parent_pipe_out = os.pipe()

        pid = os.fork()

        if pid == 0:  # Child process
            os.close(parent_pipe_out)
            os.close(parent_pipe_in)
            reverse_line(line.strip(), child_pipe_out)
            os.close(child_pipe_out)
            sys.exit(0)
        elif pid < 0:
            print("Error creating child process.")
        else:
            os.close(child_pipe_out)
            os.close(child_pipe_in)
            child_processes.append((pid, parent_pipe_out))

    for pid, parent_pipe_out in child_processes:
        os.waitpid(pid, 0)
        reversed_line = os.read(parent_pipe_out, 1024).decode()
        print(reversed_line)

if __name__ == "__main__":
    main()

