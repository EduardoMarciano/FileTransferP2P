import socket
import threading
import mysql.connector

#Procura tentativas de coneção
    # Sender  manda Sender, Chave, IP
    # Reciver manda Reciver, chave, None

def handle(client, username, Server, BD):
    
    while True:
        message = client.recv(1024).decode('utf-8')
        message = message.split(",")
        
        tipo  = message[0]
        chave = message[1]
        ip    = message[2]

        if message[0] == "Sender":
            # salva o ip e sua chave primária
            query = "INSERT INTO Sender (chave, ip) VALUES (%s, %s)"
            values = (chave, ip)

            cursor.execute(query, values)
            BD.commit()
            
        elif message[0] == "Reciver":
            try:
                # Testa para ver se o sender existe
                cursor.execute("SELECT ip FROM peers WHERE chave = %s", (chave,))

                try:
                    #Testa para ver se ele está online
                    socket.create_connection((ip, 5301))
                    
                    #Devolve o IP
                    response = f"IP do sender: {ip}"
                    client.send(response.encode('utf-8'))

                except:
                    print("Sender não online será removido")
                    query = f"DELETE FROM Sender WHERE chave = {chave}"

                    cursor.execute(query)
                    BD.commit()
                    quit()
            
            except:
                print("Sender não exite")
                quit()


        
    
#Conecta ao banco de dados
BD = mysql.connector.connect(
    host="localhost",
    user="ADMIN",
    password="CNCVx8AT*J%#cCW7SXe4q%",
    database="FileP2P"
)

cursor = BD.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS Sender (id INT AUTO_INCREMENT PRIMARY KEY, chave VARCHAR(255), ip VARCHAR(255))")

# Testa se a conexão foi bem sucedida.

if BD.is_connected():

        cursor.execute("SHOW TABLES LIKE %s", ("Sender",))
        nome_tabela = cursor.fetchone()
        print("Conexão bem sucedida com o Banco de Dados do Sistema.")
        print(f'Nome da Tabela do sender: {nome_tabela}')
    
else:

        print("Conexão mal sucedida, verifique se exite a database e o user")
        quit()
        
# Montnado o Servidor DNS
PORT = 5300
HOST = '127.0.0.1'

DNS = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

DNS.bind((HOST, PORT))
DNS.listen()

print(f"Server escutando na porta: {PORT}")

DNS.close()