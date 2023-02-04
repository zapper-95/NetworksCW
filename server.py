import socket
import sys

def start_server(port):
    serverPort = port
    print(serverPort)
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    serverSocket.bind(("127.0.0.1", serverPort))
    serverSocket.listen()
    print("The server is ready to receive")
    while True:
        client_socket, client_address = serverSocket.accept()
        print("Connected to {}".format(client_address))
        message = client_socket.recv(1024)
        print(message.decode())
        client_socket.send("dicks".encode())
        client_socket.close()
        #serverSocket.sendto("dicks", conn) 
        #message, clientAddress = serverSocket.recvfrom(1024)
        #modifiedMessage = message.decode().upper() 
        #serverSocket.sendto("modifiedMessage.encode()", clientAddress)

if __name__=="__main__":
    #take in argument port, which is then passed into start_server()
    
    start_server(int(sys.argv[1]))

