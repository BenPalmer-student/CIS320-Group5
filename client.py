import threading
import socket
from pynput.keyboard import Key, Listener
import time

disconnect_socket = threading.Event()
started_keylogger = threading.Event()

def conn():
    # Server configuration local
    HOST = 'localhost'
    PORT = 12346
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.setblocking(0)  # Set the socket to non-blocking mode
    try:
        client_socket.connect((HOST, PORT))
    except BlockingIOError:
        pass  # The socket is non-blocking, so it will raise an exception immediately
    return client_socket

def disconnect(client_socket):
    client_socket.close()

def keylogger(client_socket):
    time.sleep(1)
    client_socket.send("2".encode('utf-8'))

    while not disconnect_socket.is_set():
        try:
            data = client_socket.recv(1024)
            data = data.decode('utf-8')
            print(f"Received: {data}")
        except (BlockingIOError, ConnectionResetError, BrokenPipeError) as e:
            print("No data available at the moment.")

    print("Keylogger thread is stopping")
    return False

def on_kill(key):
    if key == Key.esc and started_keylogger.is_set():
        # Stop the keylogger when 'esc' key is released
        disconnect_socket.set()
        return False  # Stop the listener

def main():
    # client_socket = conn()
    
    # keylogger_thread = threading.Thread(target=keylogger, args=(client_socket,))
    # started_keylogger.set()
    # keylogger_thread.start()

    # # start keyboard listener thread
    # with Listener(on_release=on_kill) as listener:
    #     listener.join()

    # keylogger_thread.join()

    # if disconnect_socket.is_set():
    #     disconnect_socket.clear()
    #     disconnect(client_socket)  # Disconnect from the socket


    pass

if __name__ == "__main__":
    main()
