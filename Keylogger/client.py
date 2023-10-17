import socket

def client_program():
    # get the hostname
    port = 1236

    #ipv4 of the host machine
    host = "192.168.10.86"

    client_socket = socket.socket()
    client_socket.connect((host, port))  # connect to the server

    while True:
        # receive data stream. it won't accept data packet greater than 1024 bytes
        data = client_socket.recv(1024).decode()
        if not data:
            # if data is not received break
            break
        print("from server: " + str(data))

    client_socket.close()  # close the connection

if __name__ == '__main__':
    client_program()