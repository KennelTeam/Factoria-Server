import socket
from threading import Thread

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 10001  # The port used by the server


def receiver(sock):
    while True:
        data = s.recv(1024)
        if str(data) == "b''":
            print('Lost connection')
            break
        print(f"Received {data!r}")


def sender(sock):
    while True:
        input("Press key to send message")
        print('\n')
        with open('messages.txt') as f:
            msg = f.read().split("#\n")[1].replace('\n', ' ')
        try:
            sock.sendall(bytes(msg, encoding='utf-8'))
        except Exception as e:
            print("Error while sending!", str(e))


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    ts = Thread(target=sender, args=(s,))
    tr = Thread(target=receiver, args=(s,))
    ts.start()
    tr.start()
    ts.join()
# Have a look at messages.txt file to understand how this program works!
