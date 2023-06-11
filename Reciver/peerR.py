import socket
import os
import datetime
import time

class PeerR:
    def __init__(self, host, port, chave):
        self.host = "localhost"
        self.port = port
        self.chave = chave
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection = None
    
    
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
        sckt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        sckt.connect(("localhost", self.port))
        print("Conectado!\n")

        file_info_list = sckt.recv(1000).decode('utf-8')
        file_info_list = eval(file_info_list)

        # Exibe os detalhes dos arquivos (exceto o arquivo "sender.py") e solicita o nome do arquivo desejado
        for file_info in file_info_list:
            if file_info['name'] != "sender.py":
                print(f"Nome: {file_info['name']}\tCriação: {file_info['creation_time']}\tModificação: {file_info['modification_time']}")

        namefiles = []

        while True:
            entrada = input('Digite o nome do arquivo ou n para sair: ')
            if entrada == "n":
                break
            else:
                namefiles.append(entrada)

        # Envia o nome do arquivo ao par remoto e recebe o arquivo em blocos
        sckt.send(str(namefiles).encode())
        print(namefiles)

        for x in namefiles:
            with open(x, "wb") as file:
                while True:
                    data = sckt.recv(1024)
                    print(data)

                    file.write(data)
                    if not data:
                        print(f"Recebido: {x}")
                        break
                        
