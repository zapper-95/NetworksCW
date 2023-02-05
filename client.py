import socket
import threading
import sys



def receive_message(client_socket):
    while True:
        try:
            modifiedMessage = client_socket.recv(1024).decode()
            print(modifiedMessage)
        except:
            sys.exit(1)
            
#send message thread function
def send_message(client_socket):
    while True:
        message = input()
        if message == "q":
            client_socket.sendall(message.encode())
            return
        else:
            try:
                client_socket.sendall(message.encode())
            except:
                print("could not send message")

def start_client(username):
    serverName = "127.0.0.1"
    serverPort = 8080
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((serverName, serverPort))
    client_socket.send(username.encode()) #send username as first message to server

    receive_thread = threading.Thread(target=receive_message, args=(client_socket,))
    

    send_thread = threading.Thread(target=send_message, args=(client_socket,))

    receive_thread.start()
    send_thread.start()

    #close both threads
    receive_thread.join()
    send_thread.join()
    #stop program
    client_socket.close()


if __name__ == "__main__":
    start_client(sys.argv[1])