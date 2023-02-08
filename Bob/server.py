import socket
import sys
import threading
import os
import math

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
        current_connections[client_address][1].close()
        broadcast("{} has left the server".format(username), current_connections[client_address][1])
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
            header = client_socket.recv(1).decode()
            if header =="f":

                #read the file size from the header
                file_size = ""
                while True:
                    header = client_socket.recv(1).decode()
                    if header == "|":
                        break
                    file_size += header
                print(file_size)

                file_name = ""
                while True:
                    header = client_socket.recv(1).decode()
                    if header == "|":
                        break
                    file_name += header
                print(file_name)
                

                with open (username+"/"+file_name, "wb") as f:
                        for i in range(math.ceil(int(file_size)/1024)):
                            f.write(client_socket.recv(1024))


               
                    

            elif header == "m":
                message = client_socket.recv(1024).decode()
                server_log.append(username + ": " + message)
                print(username + ": " + message)
                broadcast(username + ": " + message, client_socket)

    except Exception as e:
        print(e)
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
        if(connection[1] != ignore):
            connection[1].send(message.encode())
    



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

                # username recieved as the first thing from the client
                username = client_socket.recv(1024).decode()

                # a list of lists of usernames and sockets for each client
                name_socket_list = [i for i in current_connections.values()] 

                # ensures no username is repeated by iterating through list of lists
                # this also means each upload folder is distinct
                if username in [i for sublist in name_socket_list for i in sublist]:
                    client_socket.send("Username already in use".encode())
                    client_socket.close()
                    continue
                
                # adds for a client address a corresponding username and socket object
                current_connections[client_address] = [username, client_socket]

                # log for server
                connected_to_message = "Connected to by {} ({})".format(client_address, username)
                server_log.append(connected_to_message)
                print(connected_to_message)

                #this is where the client will store their files

                # make sure not to overwrite any existing folder for the same user
                # if they disconnect and reconnect
                if not (os.path.exists(username)):
                    os.mkdir(username)

                
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

