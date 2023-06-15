import socket
import os
import datetime
import time
import zipfile
import hashlib

def calculate_hash(data):
    hash_object = hashlib.sha1()
    hash_object.update(data)
    
    return hash_object.hexdigest()

class PeerR:
    def __init__(self, port):
        self.port = port
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

        print(message)
        reciverDNS.close()

        # Busca as informações dentro do seu diretório
        diretorio = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),"FileTransferP2P", "Sincronizar", "ReceberArquivos")
        print(diretorio)

        files = os.listdir(diretorio)
        file_info_reciver = []

        for file_name in files:
            file_path = os.path.join(diretorio, file_name)
            file_info = {
                'name': file_name,
                'creation_time': datetime.datetime.fromtimestamp(os.path.getctime(file_path)).strftime(
                '%Y-%m-%d %H:%M:%S'),
                'modification_time': datetime.datetime.fromtimestamp(os.path.getmtime(file_path)).strftime(
                '%Y-%m-%d %H:%M:%S')
            }

            file_info_reciver.append(file_info)
        
        print(file_info_reciver)


        # Conecta-se ao par remoto e recebe a lista de informações de arquivos
        sckt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        sckt.connect((message, self.port))
        print("Conectado!\n")

        file_info_sender = sckt.recv(1000).decode('utf-8')
        file_info_sender = eval(file_info_sender)

        # Faz a sincronização da pasta
        choosenFiles = []
        for file_s in file_info_sender:
            test = True

            for file_r in file_info_reciver:

                if file_s['name'] == file_r['name']:             
                    data_s = file_s['modification_time']
                    data_r = file_r['modification_time']
                    test = False

                    if data_r<data_s:
                        print(f"Arquivo antigo substituido {file_r['modification_time']}")
                        choosenFiles.append(file_s['name'])
                    
                    else:
                         print(f"Arquivo {file_r['name']} é mais recente no diretório atual.")
            if test:
                choosenFiles.append(file_s['name'])
                print(f"Arquivo {file_s['name']} não existe")


        # Envia o nome do arquivo ao par remoto e recebe o arquivo em blocos
        sckt.send(str(choosenFiles).encode())
        print(choosenFiles)

        sender_hash = sckt.recv(1024).decode()
        zip_file_name = os.path.join(diretorio, "arquivo.zip")

        while True:
            data = sckt.recv(1024)
            
            if not data:
                print(f"Recebido")
                break

            if not 'file' in locals():
                # Cria o arquivo somente quando o primeiro bloco de dados é recebido
                file = open(zip_file_name, 'wb')

            file.write(data)

        file.close()



        if os.path.exists(zip_file_name):
            with zipfile.ZipFile(zip_file_name, "r") as zip_ref:
            
                with open(zip_file_name, "rb") as file:
                    zip_data = file.read()
                    reciver_hash = calculate_hash(zip_data)

                if reciver_hash == sender_hash:
                # Extrai todos os arquivos para o diretório
                    zip_ref.extractall(diretorio)
                    print("Arquivos extraídos com sucesso.")
                else:
                    print("arquivo Conrrompido.")
                os.remove(zip_file_name)
        else:
            print("O arquivo zip não existe.")
