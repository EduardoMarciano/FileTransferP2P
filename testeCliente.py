import socket
import random
import threading

def defineCliente():
    
    PORT = 5300
    HOST = '127.0.0.1'

    numero_aleatorio = random.randint(0, 100)

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))

    print(numero_aleatorio)
    if numero_aleatorio > 50:
            client.send("Sender,VASCO,127.0.0.1".encode('utf-8'))

    elif numero_aleatorio <= 50:
        client.send("Reciver,VASCO,127.0.0.1".encode('utf-8'))
        message = client.recv(1024).decode('utf-8')
        print(message)

defineCliente()

