import socket
import os
import datetime

class Peer:
    def __init__(self, host, port, chave):
        self.host = "localhost"
        self.port = port
        self.chave = chave
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection = None

    def send(self):
        PORT = 5300
        HOST = '177.235.144.169'

        senderDNS = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        senderDNS.connect((HOST, PORT))
        senderDNS.send((f"Sender,{self.chave}, 177.235.144.169").encode('utf-8'))

        # Inicia o servidor socket e aguarda a conexão
        self.socket.bind((self.host, self.port))

        while True:
            self.socket.listen() 
            connection, address = self.socket.accept()

            if connection:
                diretorio = os.getcwd()
                files = os.listdir(diretorio)

                file_info_list = []

                for file_name in files:
                    
                    # Obtém informações sobre os arquivos
                    file_path = os.path.join(diretorio, file_name)
                    file_info = {
                        'name': file_name,
                        'creation_time': datetime.datetime.fromtimestamp(os.path.getctime(file_path)).strftime(
                            '%Y-%m-%d %H:%M:%S'),
                        'modification_time': datetime.datetime.fromtimestamp(os.path.getmtime(file_path)).strftime(
                            '%Y-%m-%d %H:%M:%S')
                    }
                    file_info_list.append(file_info)

                # Envia a lista de informações de arquivos para o par remoto
                connection.send(str(file_info_list).encode())

                # Recebe o nome do arquivo solicitado pelo par remoto e envia o arquivo em blocos
                namefiles = connection.recv(1024).decode()
                namefiles = namefiles.split(",")

                for namefile in namefiles:
                    with open(namefile, "rb") as file:
                        for data in file.readlines():
                            connection.send(data)
                        print("Arquivo enviado!")
            else:
                continue

    def request(self, chave):
        # Conecta-se ao servidor DNS e recupera o IP
        PORT = 5300
        HOST = '177.235.144.169'

        reciverDNS = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        reciverDNS.connect((HOST, PORT))
        
        reciverDNS.send((f"Reciver,{chave}, none").encode('utf-8'))

        message = reciverDNS.recv(1024).decode('utf-8')
        message = message.split(":")
        message = message[1][1:]

        # Conecta-se ao par remoto e recebe a lista de informações de arquivos
        self.socket.connect((message, self.port))
        print("Conectado!\n")

        file_info_list = self.socket.recv(1000).decode('utf-8')
        file_info_list = eval(file_info_list)

        # Exibe os detalhes dos arquivos (exceto o arquivo "sender.py") e solicita o nome do arquivo desejado
        for file_info in file_info_list:
            if file_info['name'] != "sender.py":
                print(f"Nome: {file_info['name']}\tCriação: {file_info['creation_time']}\tModificação: {file_info['modification_time']}")

        namefile = "" 
        while True:
            entrada = input('Digite o nome do arquivo ou n para sair: ')
            if entrada == "n":
                break
            else:
                namefile = namefile+","+entrada
                 
        # Envia o nome do arquivo ao par remoto e recebe o arquivo em blocos
        self.socket.send(namefile.encode())

        lista_nameF = namefile[1:].split(",")

        for x in lista_nameF:
            with open(x, "wb") as file:
                while True:
                    data = self.socket.recv(1000000)
                    if not data:
                        break
                    file.write(data)

            print(f'{x} recebido!\n')