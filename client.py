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
        #client_run = False
        client_socket.close()

def start_client(username):
    client_run = True

    serverName = "127.0.0.1"
    serverPort = 8080
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((serverName, serverPort))
    client_socket.send(username.encode())

    send_thread = threading.Thread(target=send_message, args=(client_socket,))
    send_thread.daemon = True #make the thread a daemon so that it will exit send_messsage if the server gets shut sudddenly
    send_thread.start()

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
    start_client(sys.argv[1])