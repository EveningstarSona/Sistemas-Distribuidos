import socket
import threading
from typing import Any

HOSTNAME = '127.0.0.1'
PORT = 777

CLIENTS: dict[Any, socket.socket] = {}
THREADS: list[threading.Thread] = []

def client_thread(client: socket.socket, addr: Any):
    CLIENTS.update({addr: client})
    print(client, addr)
    data = 'data'
    while data:
        data = client.recv(4096)
        print(data.decode())
    client.close()

def main():
    s = socket.socket()
    s.bind((HOSTNAME, PORT))
    s.listen(5)
    while True:
        client_socket, client_address = s.accept()
        t = threading.Thread(target=client_thread, args=(client_socket, client_address))
        t.start()
        THREADS.append(t)

if __name__ == '__main__':
    main()