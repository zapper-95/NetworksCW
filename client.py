import socket
import threading
import sys
import getpass
def receive_message(client_socket):
    while True:
        modifiedMessage, serverAddress = client_socket.recvfrom(1024)
        if(modifiedMessage.decode()):
            print(modifiedMessage.decode())

def start_client(username):
    serverName = "127.0.0.1"
    serverPort = 8080
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket.connect((serverName, serverPort))
    clientSocket.send(username.encode())
    receive_thread = threading.Thread(target=receive_message, args=(clientSocket,))
    receive_thread.start()

    while True:
        try:
            message = input(username + ": ")
            #message = getpass.getpass("Input something: ")
            clientSocket.sendall(message.encode())
        except:
            print("Client disconnected")
            clientSocket.close()
            sys.exit()



if __name__ == "__main__":
    start_client(sys.argv[1])
