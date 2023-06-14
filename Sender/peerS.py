import socket
import os
import datetime
import time
import threading
import zipfile
import requests
import hashlib


def get_public_ip():
    response = requests.get('https://api.ipify.org?format=json')
    data = response.json()
    ip = data['ip']

    return ip


def calculate_hash(filepath):
    hash_object = hashlib.sha1()
    with open(filepath, 'rb') as file:
        while True:
            data = file.read(4096)
            if not data:
                break
            hash_object.update(data)
    return hash_object.hexdigest()

class PeerS:
    def __init__(self, port, chave):
        self.port = port
        self.chave = chave
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection = None
        self.host = socket.gethostbyname(socket.gethostname())
        print(self.host)


    def send(self):
        PORT = 5300
        HOST = '177.235.144.169'
        # Inicia o servidor socket e aguarda a conexão
        ip = get_public_ip()

        senderDNS = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        senderDNS.connect((HOST, PORT))
        senderDNS.send((f"Sender,{self.chave},{ip}").encode('utf-8'))
        senderDNS.close()

        # Inicia o servidor socket e aguarda a conexão
        self.socket.bind((self.host, self.port))

        while True:
            self.socket.listen()
            connection, address = self.socket.accept()
            if connection:
                diretorio = os.path.join(os.getcwd(), "Sincronizar")
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
                            '%Y-%m-%d %H:%M:%S'),
                    }
                    file_info_list.append(file_info)

                print(file_info_list)
                # Envia a lista de informações de arquivos para o par remoto
                connection.send(str(file_info_list).encode())
                # Recebe o nome do arquivo solicitado pelo par remoto e envia o arquivo em blocos
                namefiles = connection.recv(1024).decode()
                namefiles = eval(namefiles)
                print(namefiles)

                # Zipa os files seelcionados para o envio
                zip_file_name = os.path.join(diretorio, "pasta_selecionada.zip")

                with zipfile.ZipFile(zip_file_name, "w") as zip_file:
                    # Adiciona cada arquivo à pasta zipada
                    for namefile in namefiles:
                        file_path = os.path.join(diretorio, namefile)
                        zip_file.write(file_path, os.path.basename(file_path))
                    sender_hash = calculate_hash(zip_file)

                with open(zip_file_name, "rb") as file:
                    while True:
                        data = file.read(1024)

                        if not data:
                            break

                        connection.sendall(data)

                connection.send(sender_hash.encode('utf-8'))

                os.remove(zip_file_name)
                print("Pasta zipada enviada com sucesso.")

                connection.close()
            else:
                continue
