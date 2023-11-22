from timeit import default_timer as timer
import socket
import config

#helper func to translate raw binary addresses to readable mac addresses
def mac_addr(bytestring):
    return ':'.join('{:02x}'.format(piece) for piece in bytestring).upper()

def timefunc(func):
    def inner(*args, **kwargs):
        start = timer()
        results = func(*args, **kwargs)
        end = timer()
        message = "{} took {} seconds".format(func.__name__, end - start)
        print(message)
        return results
    return inner

def make_blocked_socket():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    return client_socket

def make_and_connect_blocked_socket_to_server():
    client_socket = make_blocked_socket()
    try:
        client_socket.connect((config.HOST, config.PORT))
        return client_socket
    except (socket.error, OSError) as e:
        print(f"Blocked socket connection failed: {e}")

def make_unblocked_socket():
    client_socket = make_blocked_socket()
    client_socket.setblocking(0)  # Set the socket to non-blocking mode
    return client_socket

def make_and_connect_unblocked_socket_to_server():
    client_socket = make_unblocked_socket()
    try:
        client_socket.connect((config.HOST, config.PORT))
    except BlockingIOError:
        pass  # The socket is non-blocking, so it will raise an exception immediately
    return client_socket

def send_to_server(socket, payload):
    socket.send(payload.encode('utf-8'))

def receive_from_server(socket):
    return socket.recv(1024).decode('utf-8')