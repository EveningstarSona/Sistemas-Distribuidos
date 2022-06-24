import socket
import threading

HOSTNAME = '127.0.0.1'
PORT = 777

def recv(s: socket.socket):
    while True:
        try:
            data = s.recv(4096)
            print(data.decode())
        except:
            print('An error ocurred.')
            s.close()
            break

def send(s: socket.socket, recv_thread: threading.Thread):
    while recv_thread.is_alive():
        message = input()
        s.send(message.encode())

def main():
    s = socket.socket()
    s.connect((HOSTNAME, PORT))
    recv_thread = threading.Thread(target=recv, args=(s,))
    recv_thread.start()
    send_thread = threading.Thread(target=send, args=(s,recv_thread))
    send_thread.start()
    recv_thread.join()

    s.close()

if __name__ == '__main__':
    main()