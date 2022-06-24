import socket
import threading
from typing import Any

HOSTNAME = '127.0.0.1'
PORT = 777

SocketAddress = tuple[str, int]

CLIENTS: dict[SocketAddress, socket.socket] = {}
NICKNAMES: dict[SocketAddress, str] = {}
THREADS: list[threading.Thread] = []

def set_client_nick(addr: Any, nickname: str):
    if nickname in NICKNAMES.values():
        return 'Nickname já escolhido.'
    old_nick = NICKNAMES[addr]
    NICKNAMES[addr] = nickname
    return f'Seu nickname é {nickname}.' if old_nick == '*' else f'{old_nick}, seu novo nickname é {nickname}'

def broadcast(addr: SocketAddress, message: str):
    for client in CLIENTS.keys():
        if CLIENTS[client] is not CLIENTS[addr]:
            CLIENTS[client].sendall(f'{NICKNAMES[addr]}: {message}'.encode())

def client_thread(client: socket.socket, addr: SocketAddress):
    CLIENTS.update({addr: client})
    NICKNAMES.update({addr: '*'})
    print(client, addr)
    client.sendall(b'Bem-vindo ao servidor! Use /nick [nickname].')
    while (data := client.recv(4096)) != b'':
        if data.decode().split()[0] == '/nick':
            client.sendall(set_client_nick(addr, " ".join(data.decode().split()[1:])).encode())
        else:
            broadcast(addr, data.decode())
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