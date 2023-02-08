import socket
import sys
import threading

run_server = True

server_socket = None

current_connections = {}
server_log = []

def close_server():

    global run_server
    global server_socket
    #clos
    run_server = False
    print("Server shutting down")
    server_socket.close()

    with open('server.log', 'w') as f:
        for line in server_log:
            f.write("{}\n".format(line))
    #throw exception to exit the server

    print("boop")


def quit_client(client_address, username):
        current_connections[client_address].close()
        
        broadcast("{} has left the server".format(username), current_connections[client_address])

        del current_connections[client_address]
        print("Client disconnected")
        return


def handle_clients(client_socket, client_address, username):
    global run_server
    connected_to_message = "Connected to from {}".format(client_address)
    server_log.append(connected_to_message)

    print(connected_to_message)
   

    client_socket.send("Welcome to the server!".encode())
    try:
        while True:
            message = client_socket.recv(1024).decode()
            if message == "q":
                quit_client(client_address, username)
                return
            elif message == "close server":
                server_socket.close()
                print("boo")
                raise RuntimeError("Server closed")        
            else:
                server_log.append(username + ": " + message)
                broadcast(username + ": " + message, client_socket)
    except RuntimeError:
        run_server = False
        return
    except:
        quit_client(client_address, username)
        return


def broadcast(message, ignore = None):
    #send a message to all clients connected to the server
    for connection in current_connections.values():
        if(connection != ignore):
            connection.send(message.encode())
    



def start_server(port):
    global run_server
    global server_socket

    serverPort = port
    print(serverPort)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    server_socket.bind(("127.0.0.1", serverPort))
    server_socket.listen()
    
    print("The server is ready to receive")
    try:
        while run_server:
                clientSocket, clientAddress = server_socket.accept()
                username = clientSocket.recv(1024).decode() #send username as first thing
                current_connections[clientAddress] = clientSocket
            
                broadcast("{} has joined the server".format(username), clientSocket)
                client_thread = threading.Thread(target=handle_clients, args=(clientSocket, clientAddress, username))
                client_thread.daemon = True
                client_thread.start()
                print(run_server)
            
    except:
        close_server()

if __name__=="__main__":
    #take in argument port, which is then passed into start_server()
    
    start_server(int(sys.argv[1]))

