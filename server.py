import socket
import threading
import ssl

HOST = 'localhost'
HTTP_PORT = 8080
HTTPS_PORT = 8443
BUFFER_SIZE = 4096

def handle_client(client_socket):
    data = client_socket.recv(BUFFER_SIZE)
    if data.startswith(b'CONNECT'):
        # HTTPS request
        client_socket.send(b'HTTP/1.1 200 Connection established\r\n\r\n')
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket = ssl.wrap_socket(server_socket, keyfile=None, certfile=None, server_side=False, cert_reqs=ssl.CERT_NONE, ssl_version=ssl.PROTOCOL_TLS)
            server_socket.connect((HOST, HTTPS_PORT))
            server_socket.send(data)
            while True:
                resp = server_socket.recv(BUFFER_SIZE)
                if len(resp) > 0:
                    client_socket.send(resp)
                else:
                    break
    else:
        # HTTP request
        client_socket.send(b'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\nConnection Established successfully')

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, HTTP_PORT))
        server_socket.listen(5)
        print(f"HTTP server listening on {HOST}:{HTTP_PORT}")

        while True:
            client_socket, addr = server_socket.accept()
            print(f"Accepted connection from {addr[0]}:{addr[1]}")
            client_handler = threading.Thread(target=handle_client, args=(client_socket,))
            client_handler.start()

if __name__ == "__main__":
    main()
