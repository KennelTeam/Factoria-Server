import socket
import ClientProcessor


HOST = '127.0.0.1'
PORT = 8081
BUFFER_SIZE = 1024

clients = {}

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.bind((HOST, PORT))
    sock.listen()
    print("socket is running")
    while True:
        connection, address = sock.accept()
        print("connected by", address)
        client_processor = ClientProcessor.ClientProcessor(address, connection)
        client_processor.start()
