import socket
import sys
import threading


current_connections = {}
def handle_clients(client_socket, client_address):
    print("Connected to from {}".format(client_address))
    client_socket.send("Welcome to the server".encode())

    while True:
        try:
            message = client_socket.recv(1024)
            #check if message is empty and if it isn't pass it to send_all()
            #if message.decode():
                #send_all(message)
                #print("bitch")
            #client_socket.send("dicks".encode())
        except:
            print("Client disconnected")
            client_socket.close()
            return


def send_to_all_connections(message):
    #write code to send a message to all clients connected to the server
    for connection in current_connections.values:
        connection.send("fuck")
    

def start_server(port):
    serverPort = port
    print(serverPort)
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    serverSocket.bind(("127.0.0.1", serverPort))
    serverSocket.listen()
    print("The server is ready to receive")
    while True:
        try:
            clientSocket, clientAddress = serverSocket.accept()
            username = clientSocket.recv(1024).decode() #send username as firs thing
            current_connections[clientAddress] = clientSocket
            clientSocket.send("Fuck")
            send_to_all_connections("{} has joined the server".format(username))
            #client_thread = threading.Thread(target=handle_clients, args=(clientSocket, clientAddress))
            #client_thread.start()
            
        except:
            print("Server shutting down")
            break
    serverSocket.close()

if __name__=="__main__":
    #take in argument port, which is then passed into start_server()
    
    start_server(int(sys.argv[1]))

