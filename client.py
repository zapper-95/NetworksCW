import socket

def start_client():
    serverName = "127.0.0.1"
    serverPort = 8080
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket.connect((serverName, serverPort))
    message = input("Input lowercase sentence: ")

    clientSocket.send(message.encode())
    modifiedMessage, serverAddress = clientSocket.recvfrom(1024)
    print(modifiedMessage.decode())
    clientSocket.close()

if __name__ == "__main__":
    start_client()
