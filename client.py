import socket
import threading
import sys


def send_message(client_socket):
    try:
        while True:
            message = input()
            if message == "q":
                client_socket.close()
                return
            client_socket.sendall(message.encode())
    except:
        print("Error, sending message")
        #close client socket, causing exception in main thread
        client_socket.close()

def start_client(username, hostname, port):
    client_run = True

    server_hostname = hostname
    server_port = port
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #attempts to connect to the server
    try:
        client_socket.connect((server_hostname, server_port))

    except:
        print("Could not connect to server")
        return

    client_socket.send(username.encode())

    #thread that constantly allows the users to send messages
    send_thread = threading.Thread(target=send_message, args=(client_socket,))
    send_thread.daemon = True 
    send_thread.start()
    #thread made a daemon, so that if an exception occurs in the main
    #thread, it will close the send_thread also

    while client_run:
        try:
            message = client_socket.recv(1024).decode()
            if(message is not None):
                print(message)
        except:
            client_socket.close()
            print("Client disconnected")
            client_run = False


if __name__ == "__main__":
    #take username, hostname and port as input and validate from the user using sys.argv
    try:
        username, hostname, port = sys.argv[1], sys.argv[2], int(sys.argv[3])
    except:
        print("Please input a username, hostname and port")
        print("try again using the following format: python client.py [username] [hostname] [port]")
        sys.exit()

    start_client(username, hostname, port)