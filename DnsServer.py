import socket
import threading
import mysql.connector

#Procura tentativas de coneção
    # Sender  manda Sender, Chave, IP
    # Reciver manda Reciver, chave, IP

def handle(client, BD, cursor):
    
    while True:
        message = client.recv(1024).decode('utf-8')
        print(message)
        message = message.split(",")
        print(message)
        if len(message)==3:
            tipo  = message[0]
            chave = message[1]
            ip    = message[2]

            if tipo == "Sender":
                # salva o ip e sua chave primária
                query = "INSERT INTO Sender (chave, ip) VALUES (%s, %s)"
                values = (chave, ip)

                cursor.execute(query, values)
                cursor.fetchall()
                BD.commit()
                
            elif tipo == "Reciver":
                try:
                    # Resgata o IP do sender
                    cursor.execute("SELECT ip FROM Sender WHERE chave = %s", (chave,))
                    result = cursor.fetchone()
                    cursor.fetchall()

                    sender_ip = result[0]

                    try:
                        #Testa para ver se ele está online
                        socket.create_connection((sender_ip, 5300))
                        
                        #Devolve o IP
                        response = f"IP do sender: {sender_ip}"
                        client.send(response.encode('utf-8'))

                    except  ConnectionError:
                        print("Sender offline será removido")

                        query = "DELETE FROM Sender WHERE chave = %s"
                        cursor.execute(query, (chave,))
                        cursor.fetchall()

                        BD.commit()
                        quit()
                
                except:
                    print("Sender não exite")
                    client.send("Sender não existe".encode('utf-8'))
                    quit()

            else:
                print("Tipo de pedido não existe")

        else:
            print("Recebemos lixo")
            quit()

def tratamento_cliente(client):
    handle(client, BD, cursor)
    client.close()


#Conecta ao banco de dados
BD = mysql.connector.connect(
    host="localhost",
    user="ADMIN",
    password="CNCVx8AT*J%#cCW7SXe4q%",
    database="FileP2P"
)

cursor = BD.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS Sender (id INT AUTO_INCREMENT PRIMARY KEY, chave VARCHAR(255), ip VARCHAR(255))")
cursor.fetchone()
# Testa se a conexão foi bem sucedida.

if BD.is_connected():

        cursor.execute("SHOW TABLES LIKE %s", ("Sender",))
        nome_tabela = cursor.fetchone()
        print("Conexão bem sucedida com o Banco de Dados do Sistema.")

        if nome_tabela:
            print("Tabela 'Sender' existe no banco de dados.")
        else:
            print("Tabela 'Sender' não existe no banco de dados.")
    
else:
        print("Conexão mal sucedida, verifique se exite a database e o user")
        quit()

cursor.fetchall()
        
# Montnado o Servidor DNS
PORT = 5300
HOST = '127.0.0.1'

DNS = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

DNS.bind((HOST, PORT))
DNS.listen()

print(f"Server escutando na porta: {PORT}")

while True:
        client, address = DNS.accept()

        print(f"Nova conexão estabelecida: {address[0]}:{address[1]}")

        # Inicia uma nova thread para lidar com o cliente
        thread = threading.Thread(target=tratamento_cliente, args=(client,))
        thread.start()

cursor.close()
BD.close()
DNS.close()