import socket
import os
import datetime
import time

class PeerS:
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
        senderDNS.send((f"Sender,{self.chave}, {self.host}").encode('utf-8'))

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
                namefiles = eval(namefiles)
                print(namefiles)
                
                for namefile in namefiles:
                    with open(namefile, "rb") as file:
                        while True:
                            data = file.read(1024)
                            
                            if not data:
                                break

                            connection.sendall(data)

                    print(f"Enviado: {namefile}")
                connection.close()
            else:
                continue