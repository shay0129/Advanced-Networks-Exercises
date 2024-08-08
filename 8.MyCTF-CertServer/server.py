import ssl
import socket
import threading
import random
import string
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.x509.oid import NameOID, ExtensionOID

HOST = '0.0.0.0'
PORT = 65432

clients = []
certified_clients = []
clients_connected = False  # Variable to track if any clients are connected

# Generate a random encryption key
def generate_encryption_key(length=16) -> str:
    """Generates a random encryption key."""
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for i in range(length))

def verify_certificate(cert) -> bool:
    """Verifies the certificate's common name and subject alternative name."""
    try:
        # Load the certificate
        cert = x509.load_pem_x509_certificate(cert, default_backend())

        # Check common name (CN)
        common_name = cert.subject.get_attributes_for_oid(NameOID.COMMON_NAME)[0].value
        if common_name != "Pasdaran.local":
            return False

        # Check subject alternative name (SAN)
        ext = cert.extensions.get_extension_for_oid(ExtensionOID.SUBJECT_ALTERNATIVE_NAME)
        san = ext.value.get_values_for_type(x509.DNSName)
        if "Pasdaran.local" not in san:
            return False

        return True
    except Exception as e:
        print(f"Error verifying certificate: {e}")
        return False

def handle_client(client_socket: ssl.SSLSocket) -> None:
    """Handles the communication with a connected client."""
    global clients_connected

    try:
        # Get peer name (remote address)
        peername = client_socket.getpeername()
        peer_ip = peername[0]

        # Reject connections using IP addresses instead of the domain
        if peer_ip == '127.0.0.1':
            client_socket.sendall(b"400 Bad Request")
            return

        # Check if the client has a certificate
        client_cert = client_socket.getpeercert(binary_form=True)
        if client_cert and verify_certificate(client_cert):
            certified_clients.append(client_socket)
            client_socket.sendall(b"200 OK")
            client_socket.sendall(b"resource.png")
        else:
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
            print(f"Encryption key: {encryption_key}")
            clients_connected = False

def setup_ssl_context() -> ssl.SSLContext:
    """Sets up the SSL context for the server."""
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    try:
        context.load_cert_chain(certfile='localhost.crt', keyfile='localhost.key')
    except Exception as e:
        print(f"Error loading certificate or key: {e}")
        raise
    context.verify_mode = ssl.CERT_REQUIRED  # Client certificate is required
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
