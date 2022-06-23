import socket

HOSTNAME = '127.0.0.1'
PORT = 777

def main():
    s = socket.socket()
    s.connect((HOSTNAME, PORT))
    s.sendall(b'Estou vivo!')
    while (data := s.recv(4096)):
        s.sendall(input().encode())
        print(data.decode())
    s.close()

if __name__ == '__main__':
    main()