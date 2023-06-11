import socket
import os
import datetime
import time

class Reciver:
    def __init__(self, host, port):
        self.host = '192.168.0.5'
        self.port = port

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
            data = None
            while data == None:
                data = sckt.recv(5 * 1024 * 1024)
                time.sleep(5)
                with open(x, "wb") as file:
                    print(f'{x} recebido!\n')