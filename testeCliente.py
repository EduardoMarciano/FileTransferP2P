import socket
import random
import threading

PORT = 5300
HOST = '192.168.0.5'

while True:
        escolha = input()

        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((HOST, PORT))

        if escolha == "Sender":
                client.send("Sender,TARC4, 288.8.8.8".encode('utf-8'))
        
        elif escolha == "Reciver":
                client.send("Reciver,TARwC4, none".encode('utf-8'))

        else:
                print("Entrada Errada")
                continue

        message = client.recv(1024).decode('utf-8')
        print(message)