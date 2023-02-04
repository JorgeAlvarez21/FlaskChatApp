import socket
import time
import threading

# host = socket.gethostbyname(socket.gethostname())
def server_connect():
    host = socket.gethostname() #localhost
    port = 5050
    server_socket = socket.socket()

    server_socket.bind((host, port))

    server_socket.listen(2)
    conn, address = server_socket.accept()
    print("Connection started from: " + str(address))
    while True:
        data = conn.recv(2000).decode()
        if not data:
            break
        print("from connected user: " + str(data))
        data = input(' -> ')
        conn.send(data.encode())  

    conn.close()  # close the connection