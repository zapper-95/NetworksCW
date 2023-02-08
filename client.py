import socket
import threading
import sys


def send_message(client_socket):
    try:
        while True:
            message = input()

            if message == "q": # so the user can quit
                client_socket.close()
                return
            elif message[:6] == "upload":
                
                filename = message[7:] #get the filename from the message

                #open the file, and read its contents into a variable
                try:
                    #read in the bytes of the file
                    with open(filename, 'rb') as f: 
                        file_contents = f.read()

                    #header contains message type, file size and filename
                    header = ("f" + str(len(file_contents)) + "|" + filename + "|").encode()
                except:
                    print("File not found")
                    continue

                client_socket.sendall(header + file_contents)
            else: #if the message is not a file, send it as a normal message
                header = "m".encode()
                client_socket.sendall(header + message.encode())
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
            if(message is not None and message != ""):
                print(message)
            else: #the message returned should not be empty
                raise Exception
        except:
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