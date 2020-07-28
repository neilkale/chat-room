# To be sent to clients as a .exe
import socket
import threading
import sys

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    f = open("server_address.txt", 'r')
    IP = f.readline()
    PORT = int(f.readline())

    #IP = "192.168.1.186"
    #PORT = 22503

    client_socket.connect((IP, PORT))
    client_socket.setblocking(False)

    t1 = threading.Thread(target = read_from_server, args= (client_socket,))
    t2 = threading.Thread(target = write_to_server, args = (client_socket,))
    t1.start()
    t2.start()

def read_from_server(client_socket):
    while True:
        try:
            dataFromServer = client_socket.recv(2048)
            print('\r' + dataFromServer.decode())
        except:
            continue

def write_to_server(client_socket):
    while True:
        message = input()
        if(message == "quit"):
            client_socket.close()
            sys.exit()
        else:
            client_socket.send(message.encode('utf-8'))

if(__name__ == "__main__"):
    main()
