import socket

HOST = 'localhost'
PORT = 8080
BUFFER_SIZE = 4096

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))
    client_socket.send(b'GET / HTTP/1.1\r\nHost: www.example.com\r\n\r\n')
    response = client_socket.recv(BUFFER_SIZE)
    print(response.decode())

if __name__ == "__main__":
    main()
