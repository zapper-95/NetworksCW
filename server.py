import socket
import sys
import threading


current_connections = {}
def handle_clients(client_socket, client_address, username):
    print("Connected to from {}".format(client_address))
    client_socket.send("Welcome to the server!".encode())
    try:
        while True:

            message = client_socket.recv(1024)
            if message.decode():
                print(message.decode())
                send_to_all_connections(username + ": " + message.decode(), client_socket)
    except:
        del current_connections[client_address]
        send_to_all_connections("{} has left the server".format(username), client_socket)
        print("Client disconnected")
        client_socket.close()
        return


def send_to_all_connections(message, ignore = None):
    #write code to send a message to all clients connected to the server
    for connection in current_connections.values():
        if(connection != ignore):
            connection.send(message.encode())
    



def start_server(port):
    serverPort = port
    print(serverPort)
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    serverSocket.bind(("127.0.0.1", serverPort))
    serverSocket.listen()
    print("The server is ready to receive")
    try:
        while True:
                clientSocket, clientAddress = serverSocket.accept()
                username = clientSocket.recv(1024).decode() #send username as firs thing
                current_connections[clientAddress] = clientSocket
            
                send_to_all_connections("{} has joined the server".format(username), clientSocket)
                client_thread = threading.Thread(target=handle_clients, args=(clientSocket, clientAddress, username))
                client_thread.start()

            
    except:
        print("Server shutting down")
    serverSocket.close()

if __name__=="__main__":
    #take in argument port, which is then passed into start_server()
    
    start_server(int(sys.argv[1]))

