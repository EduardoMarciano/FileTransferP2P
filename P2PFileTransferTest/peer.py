import socket

class Peer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection = None

    def send(self):
        self.socket.bind((self.host,self.port))
        self.socket.listen(1)
        connection, address = self.socket.accept()
        namefile = connection.recv(1024).decode()
        with open(namefile, "rb") as file:
            for data in file.readlines():
                connection.send(data)
            print("Arquivo enviado!")


    def request(self):
        self.socket.connect((self.host, self.port))
        print("Conectado!\n")
        namefile = str(input('Digite o nome do arquivo: '))
        self.socket.send(namefile.encode())
        with open(namefile, "wb") as file:
            while True:
                data = self.socket.recv(1000000)
                if not data:
                    break
                file.write(data)

        print(f'{namefile} recebido!\n')
