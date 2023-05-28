import socket
import threading

class Peer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection = None
        
    def connect(self, host, port):
        while True:
            try:
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                #self.connection = self.socket.connect((host, port))
                self.socket.connect((host, port))
                print("Conexão bem sucedida.")
                break
            except socket.error as e:
                print("Falha na conexão.", f"Erro: {e}", sep='\n')
            
    def listen(self):
        self.socket.bind(('', self.port))
        self.socket.listen(1)
        
        while True:
            connection, _ = self.socket.accept() #_ = address
            self.connection = connection
            
            message = self.connection.recv(4096)
            
            if not message:
                break
            else:
                print(message.decode())
            
    def send(self, message):
        try:
            self.socket.send(message.encode())
        except socket.error as e:
            print("Erro ao enviar mensagem", f"Erro: {e}", sep='\n')
            
    def start(self):
        listen_thread = threading.Thread(target=self.listen)
        listen_thread.start()
"""
Testando se funciona
"""
peer1 = Peer("localhost", 8888)
peer2 = Peer("localhost", 8883)
peer1.start()
peer2.start()

try:
    peer1.connect("localhost", 8883)
    peer1.send('aaa')
except socket.error as e:
    print(f'Erro:{e}')