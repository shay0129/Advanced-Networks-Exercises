import ssl
import socket
import threading
import random
import string

HOST = '0.0.0.0'
PORT = 65432

clients = []
certified_clients = []
clients_connected = False  # Variable to track if any clients are connected

def generate_encryption_key(length=16)->str:
    """Generates a random encryption key."""
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for i in range(length))

def handle_client(client_socket: socket.socket)->None:
    """Handles the communication with a connected client."""
    global clients_connected

    try:
        # Send an encryption key to the client
        encryption_key = generate_encryption_key()
        client_socket.sendall(encryption_key.encode())

        # Check if the client has a certificate
        client_cert = client_socket.getpeercert()
        if client_cert:
            certified_clients.append(client_socket)
        
        while True:
            message = client_socket.recv(1024).decode()
            if not message:
                break

            print(f"Received message: {message}")
            if message == "GET RESOURCE":
                # Send resource to all certified clients and the requesting client
                if certified_clients:
                    for client in certified_clients:
                        if client != client_socket:
                            client.sendall(b"200 OK")
                            client.sendall(b"resource.png")
                # Send resource to the client with a valid certificate
                client_socket.sendall(b"200 OK")
                client_socket.sendall(b"resource.png")
            else:
                # No certified clients, just send to the requestor
                client_socket.sendall(b"400 Bad Request")

    except Exception as e:
        print(f"Error handling client: {e}")
    finally:
        client_socket.close()
        clients.remove(client_socket)
        if client_socket in certified_clients:
            certified_clients.remove(client_socket)
        
        # Update clients_connected status
        if not clients:
            # Encryption code:
            # wait 10 seconds before printing the key
            import time
            time.sleep(10)
            # Print the key when no clients are connected
            print(f"کد رمزگذاری: {encryption_key}")
            clients_connected = False

def setup_ssl_context()->ssl.SSLContext:
    """Sets up the SSL context for the server."""
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    try:
        context.load_cert_chain(certfile='localhost.crt', keyfile='localhost.key')
    except Exception as e:
        print(f"Error loading certificate or key: {e}")
        raise
    context.verify_mode = ssl.CERT_NONE  # Client certificate is optional
    return context

def main():
    """Main function to start the server."""
    global clients_connected
    context = setup_ssl_context()

    # Create and wrap the server socket with SSL
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen()
        server_socket = context.wrap_socket(server_socket, server_side=True)

        print(f"Server listening on {HOST}:{PORT}")

        while True:
            client_socket, addr = server_socket.accept()
            clients.append(client_socket)
            clients_connected = True  # Update status when a client connects
            print(f"New connection from {addr}")
            threading.Thread(target=handle_client, args=(client_socket,)).start()

if __name__ == "__main__":
    main()
