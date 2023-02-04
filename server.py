import socket
import sys
import threading

def handle_clients(client_socket, client_address):
    print("Connected to {}".format(client_address))
    message = client_socket.recv(1024)
    print(message.decode())
    client_socket.send("dicks".encode())
    client_socket.close()

def start_server(port):
    serverPort = port
    print(serverPort)
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    serverSocket.bind(("127.0.0.1", serverPort))
    serverSocket.listen()
    print("The server is ready to receive")
    while True:
        clientSocket, clientAddress = serverSocket.accept()
        client_thread = threading.Thread(target=handle_clients, args=(clientSocket, clientAddress))
        client_thread.start()

if __name__=="__main__":
    #take in argument port, which is then passed into start_server()
    
    start_server(int(sys.argv[1]))

