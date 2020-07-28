import socket
import select
import sys
from threading import Thread
from requests import get 

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print("Server socket created.")

    IP = socket.gethostbyname(socket.gethostname())
    f = open("server_address.txt", "w")
    f.write(IP)
    f.write('\n')
    PORT = 22503
    f.write(str(PORT))
    f.close()

    #IP = "192.168.1.186"
    #PORT = 35743

    server_socket.bind((IP, PORT))
    server_socket.listen(40)

    print(f"Listening for connections on {IP}:{PORT}...")

    sockets_list = []
    clients_list = {}

    def clientthread(client_socket, client_address):

        welcome_message = "Hey there! Type your message below, \'quit\' when you'd like to exit. \nWhatcha name, man: "
        welcome_message = welcome_message.encode()
        client_socket.send(welcome_message)
        clients_list[client_address] = client_socket.recv(2048).decode()

        while True:
            try:
                message = client_socket.recv(2048).decode()
                if message:
                    message_to_send = "<" + str(clients_list[client_address]) + "> " + str(message)
                    print(message_to_send, flush = True)
                    broadcast(message_to_send, client_socket)
                else:
                    remove(client_socket)
            except:
                continue

    def broadcast(message, sending_socket):
        for client_sockets in sockets_list:
            if client_sockets != sending_socket:
                try:
                    client_sockets.send(message.encode('utf-8'))
                except:
                    remove(client_sockets)
                    client_sockets.close()                

    def remove(client_socket):
        if client_socket in sockets_list:
            sockets_list.remove(client_socket)
            clients_list.pop(client_socket)
            print(f"Removed a connection", flush = True)

    while True:
        (client_socket, client_address) = server_socket.accept()
        sockets_list.append(client_socket)
        print(f"Accepted a connection request from {client_address[0]}:{client_address[1]}")
        t = threading.Thread(target=clientthread, args=(client_socket, client_address))
        t.start()
        
    server_socket.close()

if __name__ == "__main__":
    main()
