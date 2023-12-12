import socket
import threading

class Server:
    def __init__(self, host='0.0.0.0', port=55555):
        self.host = host
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen()
        self.clients = []
        self.nicknames = []
        self.rooms = {"1": [], "2": [], "3": []}

    def broadcast(self, message, room):
        for client in self.rooms[room]:
            client.send(message)

    def handle(self, client, room, nickname):
        while True:
            try:
                message = client.recv(1024).decode('ascii')
                self.broadcast(f'{nickname}: {message}'.encode('ascii'), room)  # Codifica el mensaje antes de enviarlo
            except:
                index = self.clients.index(client)
                self.clients.remove(client)
                client.close()
                nickname = self.nicknames[index]
                self.nicknames.remove(nickname)
                self.broadcast(f'{nickname} left the chat!'.encode('ascii'), room)
                break


    def receive(self):
        while True:
            client, address = self.server.accept()
            print(f'Connected with {str(address)}')

            client.send('NICK'.encode('ascii'))
            nickname = client.recv(1024).decode('ascii')
            self.nicknames.append(nickname)
            self.clients.append(client)

            print(f'Nickname of the client is {nickname}!')
            
            client.send(f'Select your room: {list(self.rooms.keys())}'.encode('ascii'))
            room = client.recv(1024).decode('ascii')
            
            if room in self.rooms:
                self.join_room(client, room, nickname)
                self.broadcast(f'{nickname} joined the chat!'.encode('ascii'), room)
                client.send('Connected to the server!'.encode('ascii'))
                
                thread = threading.Thread(target=self.handle, args=(client, room, nickname))
                thread.start()
            else:
                client.send('Invalid room. Disconnecting...'.encode('ascii'))
                client.close()

    def join_room(self, client, room_name, nickname):
        if room_name not in self.rooms:
            self.rooms[room_name] = []
        self.rooms[room_name].append(client)
        client.send(f'Has unido a la sala {room_name}'.encode('ascii'))

    def leave_room(self, client, room_name):
        if room_name in self.rooms:
            self.rooms[room_name].remove(client)
            client.send(f'Has salido de la sala {room_name}'.encode('ascii'))

server = Server()
server.receive()
