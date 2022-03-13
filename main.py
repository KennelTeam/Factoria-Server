import socket
import ClientProcessor


HOST = '0.0.0.0'
PORT = 10001
BUFFER_SIZE = 1024

clients = {}

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind((HOST, PORT))
sock.listen()
print("socket is running")
while True:
    connection, address = sock.accept()
    print("connected by", address)
    client_processor = ClientProcessor.ClientProcessor(address, connection)
    client_processor.start()
