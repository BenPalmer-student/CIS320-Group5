from timeit import default_timer as timer

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
