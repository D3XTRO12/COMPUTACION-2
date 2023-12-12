import socket
import threading

class Client:
    def __init__(self, host='0.0.0.0', port=55555):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((host, port))

    def receive(self):
        while True:
            try:
                message = self.client.recv(1024).decode('ascii')
                print(message)
            except:
                print("¡Desconectado del servidor!")
                self.client.close()
                break

    def write(self):
        while True:
            message = input(">> ")
            if message.startswith('/join'):
                room_name = message[6:]
                self.client.send(f'/join {room_name}'.encode('ascii'))
            elif message.startswith('/leave'):
                room_name = message[7:]
                self.client.send(f'/leave {room_name}'.encode('ascii'))
            else:
                self.client.send(message.encode('ascii'))

    def run(self):
        receive_thread = threading.Thread(target=self.receive)
        receive_thread.start()

        write_thread = threading.Thread(target=self.write)
        write_thread.start()

client = Client()
client.run()
