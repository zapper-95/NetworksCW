import socket
import sys
import threading

current_connections = {}
server_log = []



def handle_input(server_socket):
    while True:
        user_input = input()
        if user_input == "q":
            server_socket.close()
            break


def close_server(server_socket):

    print("Server shutting down")

    #closes the server socket if it is still open
    #this will cause an exception for all clients, causing them to disconnect
    #withinside their python script
    if(server_socket.fileno() != -1):
        server_socket.close()

    with open('server.log', 'w') as f:
        for line in server_log:
            f.write("{}\n".format(line))


def quit_client(client_address, username):

        # handle disconnection for client
        current_connections[client_address].close()
        broadcast("{} has left the server".format(username), current_connections[client_address])
        del current_connections[client_address]
        

        # log for the server
        disconnect_by_message = "Disconnected by {} ({})".format(client_address, username)
        print(disconnect_by_message)
        server_log.append(disconnect_by_message)
        return


def handle_client(client_socket, client_address, username):

    broadcast("{} has joined the server".format(username), client_socket)
   

    client_socket.send("Welcome to the server!".encode())
    try:
        while True:
            message = client_socket.recv(1024).decode()
            if message == "q": #lets the client quit
                quit_client(client_address, username)
                return     
            else:
                server_log.append(username + ": " + message)
                print(username + ": " + message)
                broadcast(username + ": " + message, client_socket)
    except:
        #if there is an exception, disconnect the client

        # this would occur if a client leaves due to connection lost
        # as client_socket.recv would throw an exception
        quit_client(client_address, username)
        return


def broadcast(message, ignore = None):
    # send a message to all clients connected to the server
    # can add a client to not to send to (i.e the person
    # who sent the message)
    for connection in current_connections.values():
        if(connection != ignore):
            connection.send(message.encode())
    



def start_server(port):
    try:
        serverPort = port
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        server_socket.bind(("127.0.0.1", serverPort))
        server_socket.listen()
    except:
        print("Could not start server (most likely port is already in use)")
        return

    # thread to handle input to close the server
    input_thread = threading.Thread(target=handle_input, args=(server_socket,))
    input_thread.daemon = True
    input_thread.start()

    
    print("The server is ready to receive")
    try:
        # this while loop, loops for each new client joining
        while True:
                client_socket, client_address = server_socket.accept()

                # username sent as the first thing
                username = client_socket.recv(1024).decode() 
                current_connections[client_address] = client_socket

                # log for server
                connected_to_message = "Connected to {} ({})".format(client_address, username)
                server_log.append(connected_to_message)
                print(connected_to_message)
        

                # when accepting new user, run a new handle_client thread
                client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address, username))
                client_thread.daemon = True
                client_thread.start()
            
    except:
        close_server(server_socket)

if __name__=="__main__":
    try:
        port = int(sys.argv[1]) 
    except:
        print("Please enter a port number")
        sys.exit(1)
    # take in argument port, which is then passed into start_server()    
    start_server(int(sys.argv[1]))

