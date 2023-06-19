import socket
import random
import threading
PORT = 5300
HOST = '177.235.144.169'
while True:
        escolha = input()
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((HOST, PORT))
        if escolha == "Sender":
                client.send("Sender,2121, 9 99.9 99.99.L".encode('utf-8'))
        
        elif escolha == "Reciver":
                client.send("Reciver,2121, none".encode('utf-8'))
                
                print(client.recv(1024).decode("utf-8"))
        else:
                print("Entrada Errada")
                continue