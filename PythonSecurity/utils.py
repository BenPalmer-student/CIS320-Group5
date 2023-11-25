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

def create_socket():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    return client_socket

def connect_blocked_socket():
    client_socket = create_socket()
    try:
        client_socket.connect((config.CLIENT_HOST, config.CLIENT_PORT))
        return client_socket
    except (socket.error, OSError) as e:
        print(f"Blocked socket connection failed: {e}")
        return None

def connect_unblocked_socket():
    client_socket = create_socket()
    client_socket.setblocking(0)  # Set the socket to non-blocking mode
    try:
        client_socket.connect((config.CLIENT_HOST, config.CLIENT_PORT))
        return client_socket
    except BlockingIOError:
        return client_socket # The socket is non-blocking, so it will raise an exception immediately
    except (socket.error, OSError) as e:
        print(f"Unblocked socket connection failed: {e}")
        return None

def send_to_server(socket, payload):
    socket.send(payload.encode('utf-8'))

def receive_from_server(socket):
    return socket.recv(1024).decode('utf-8')