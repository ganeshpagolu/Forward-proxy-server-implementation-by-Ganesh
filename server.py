import argparse
import socket
import ssl
import sys
from _thread import *
from decouple import config

try:
    listening_port = config('PORT', cast=int)
except KeyboardInterrupt:
    print("\n[*] User has requested an interrupt")
    print("[*] Application Exiting.....")
    sys.exit()

parser = argparse.ArgumentParser()
parser.add_argument('--max_conn', help="Maximum allowed connections", default=5, type=int)
parser.add_argument('--buffer_size', help="Number of samples to be used", default=8192, type=int)
args = parser.parse_args()
max_connection = args.max_conn
buffer_size = args.buffer_size

def start():    # Main Program
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(('', listening_port))
        sock.listen(max_connection)
        print("[*] Server started successfully [ %d ]" % (listening_port))
    except Exception as e:
        print("[*] Unable to Initialize Socket")
        print(e)
        sys.exit(2)

    while True:
        try:
            conn, addr = sock.accept()  # Accept connection from client browser
            data = conn.recv(buffer_size)  # Receive client data
            start_new_thread(conn_string, (conn, data, addr))  # Starting a thread
        except KeyboardInterrupt:
            sock.close()
            print("\n[*] Graceful Shutdown")
            sys.exit(1)

def conn_string(conn, data, addr):
    try:

        first_line = data.split(b'\n')[0]

        url = first_line.split()[1]

        http_pos = url.find(b'://')  # Finding the position of website
        if (http_pos == -1):
            temp = url
        else:
            temp = url[(http_pos + 3):]

        port_pos = temp.find(b':')

        webserver_pos = temp.find(b'/')
        if webserver_pos == -1:
            webserver_pos = len(temp)
        webserver = ""
        port = -1
        if (port_pos == -1 or webserver_pos < port_pos):
            port = 80
            webserver = temp[:webserver_pos]
        else:
            port = int((temp[(port_pos + 1):])[:webserver_pos - port_pos - 1])
            webserver = temp[:port_pos]
        print(data)
        if port == 443:  # HTTPS connection
            proxy_https_server(webserver, port, conn, addr, data)
        else:  # HTTP connection
            proxy_http_server(webserver, port, conn, addr, data)
    except Exception:
        pass

def proxy_http_server(webserver, port, conn, addr, data):
    try:
        print(data)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((webserver, port))
        sock.send(data)

        while 1:
            reply = sock.recv(buffer_size)
            if (len(reply) > 0):
                conn.send(reply)

                dar = float(len(reply))
                dar = float(dar / 1024)
                dar = "%.3s" % (str(dar))
                dar = "%s KB" % (dar)
                print("[*] Request Done: %s => %s <=" % (str(addr[0]), str(dar)))

            else:
                break

        sock.close()
        conn.close()
    except socket.error:
        sock.close()
        conn.close()
        print(sock.error)
        sys.exit(1)

def proxy_https_server(webserver, port, conn, addr, data):
    try:
        print(data)
        context = ssl.create_default_context()
        with socket.create_connection((webserver, port)) as client_sock:
            with context.wrap_socket(client_sock, server_hostname=webserver) as ssl_client_sock:
                ssl_client_sock.send(data)
                while True:
                    reply = ssl_client_sock.recv(buffer_size)
                    if len(reply) > 0:
                        conn.send(reply)

                        dar = float(len(reply))
                        dar = float(dar / 1024)
                        dar = "%.3s" % (str(dar))
                        dar = "%s KB" % (dar)
                        print("[*] Request Done: %s => %s <=" % (str(addr[0]), str(dar)))
                    else:
                        break
    except socket.error:
        conn.close()
        print(socket.error)
        sys.exit(1)


if __name__ == "__main__":
    start()
