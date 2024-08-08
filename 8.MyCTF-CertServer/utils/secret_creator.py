import os
import socket
import ssl

# Set the path for the SSL key log file
os.environ['SSLKEYLOGFILE'] = 'sslkeylogfile.log'

# Set up server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', 443))
server_socket.listen(5)
print("Server listening on port 443")

# Load the SSL context with correct paths to certificate files
context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
context.load_cert_chain(certfile="Pasdaran.local.crt", keyfile="Pasdaran.local.key")

# Accept connections
while True:
    client_socket, addr = server_socket.accept()
    print(f"Connection from {addr}")

    # Wrap the socket with SSL
    ssl_socket = context.wrap_socket(client_socket, server_side=True)

    # Handle the SSL/TLS connection
    try:
        print("SSL/TLS connection established")
        data = ssl_socket.recv(1024)
        print("Received:", data)
        ssl_socket.sendall(b"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\nHello World")
    finally:
        ssl_socket.close()
        print("Connection closed")
