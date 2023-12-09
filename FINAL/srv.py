import socket
import threading

conn_usr = set()

def handle_user(conn, addr):
   try:
       while True:
           message = conn.recv(1024)
           if not message:
               break
           decoded_msg = message.decode('utf-8')
           print(f"Message received {addr}: {decoded_msg}")

           response = f"Server: Received your message - {decoded_msg}\n"
           conn.send(response.encode('utf-8'))

   except ConnectionResetError:
       print(f"Connection reset by peer {addr}")
   finally:
       print(f"User {addr} disconnected.")
       conn_usr.remove(conn)
       conn.close()

def accept_conn(server):
   while True:
       conn, addr = server.accept()
       conn_usr.add(conn)
       print(f"User {addr} connected.")
       threading.Thread(target=handle_user, args=(conn, addr)).start()

def main():
   server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   server.bind(('0.0.0.0', 3000))
   server.listen(100)
   print("Waiting for connections...")
   accept_conn(server)

if __name__ == "__main__":
   main()
