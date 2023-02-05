import socket
import threading
import sys
client_connected = True

def receive_message(client_socket):
    global client_connected
    while True:
        try:
            modifiedMessage = client_socket.recv(1024).decode()
            if(modifiedMessage):
                print(modifiedMessage)
        except:
            client_socket.close()
            print("Client disconnected")
            client_connected = False
            return

def start_client(username):
    serverName = "127.0.0.1"
    serverPort = 8080
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket.connect((serverName, serverPort))
    clientSocket.send(username.encode())

    receive_thread = threading.Thread(target=receive_message, args=(clientSocket,))
    receive_thread.start()

    while client_connected:
        message = input()
        if message == "q":
            clientSocket.close()
            receive_thread.join()
            sys.exit()

        clientSocket.sendall(message.encode())



if __name__ == "__main__":
    start_client(sys.argv[1])