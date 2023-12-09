import socket
import threading

def send_msg(conn, msg):
   conn.send(msg.encode('utf-8'))

def receive_msg(conn):
   while True:
       try:
           msg = conn.recv(1024)
           if not msg:
               break
           print(f"Message received: {msg.decode('utf-8')}")
       except ConnectionResetError:
           print("Receive task cancelled.")
       except Exception as e:
           print(f"Error in receive_msg: {e}")
       finally:
           print("Exiting receive_msg loop")

def read_user_entry(conn):
   while True:
       msg = input(">> ")
       if msg == "exit":
           break
       send_msg(conn, f'{msg}\n')
   print("Exiting read_user_entry loop")

def main():
   name = input("Put your name: ")
   conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   conn.connect(('localhost', 3000))

   input_future = threading.Thread(target=input, args=(">> ",))
   input_future.start()

   threading.Thread(target=receive_msg, args=(conn,)).start()
   threading.Thread(target=read_user_entry, args=(conn,)).start()

   try:
       print("Connection successfully!, you can now send messages.")
       while True:
           pass
   except KeyboardInterrupt:
       conn.close()
   finally:
       print("Exiting main loop")

if __name__ == '__main__':
   main()
