import socket
import os
import datetime

class Peer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection = None

    def send(self):
        self.socket.bind((self.host, self.port))
        self.socket.listen(1)
        connection, address = self.socket.accept()
        diretorio = os.getcwd()
        files = os.listdir(diretorio)

        file_info_list = []
        for file_name in files:
            file_path = os.path.join(diretorio, file_name)
            file_info = {
                'name': file_name,
                'creation_time': datetime.datetime.fromtimestamp(os.path.getctime(file_path)).strftime(
                    '%Y-%m-%d %H:%M:%S'),
                'modification_time': datetime.datetime.fromtimestamp(os.path.getmtime(file_path)).strftime(
                    '%Y-%m-%d %H:%M:%S')
            }
            file_info_list.append(file_info)

        connection.send(str(file_info_list).encode())

        namefile = connection.recv(1024).decode()
        with open(namefile, "rb") as file:
            for data in file.readlines():
                connection.send(data)
            print("Arquivo enviado!")

    def request(self):
        self.socket.connect((self.host, self.port))
        print("Conectado!\n")

        file_info_list = self.socket.recv(1000)
        file_info_list = file_info_list.decode('utf-8')
        file_info_list = eval(file_info_list)

        for file_info in file_info_list:
            if file_info['name'] != "sender.py":
                print(f"Nome: {file_info['name']}\tCriação: {file_info['creation_time']}\tModificação: {file_info['modification_time']}")

        namefile = str(input('Digite o nome do arquivo: '))
        self.socket.send(namefile.encode())

        with open(namefile, "wb") as file:
            while True:
                data = self.socket.recv(1000000)
                if not data:
                    break
                file.write(data)

        print(f'{namefile} recebido!\n')