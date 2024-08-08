import ssl
import socket

SERVER_DOMAIN = 'Pasdaran.local'
SERVER_PORT = 65432

def main():
    # Create an SSL context
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    context.load_verify_locations(cafile='Pasdaran.local.crt')
    context.load_cert_chain(certfile='Pasdaran.local.crt', keyfile='Pasdaran.local.key')

    # Connect to the server using the domain
    with socket.create_connection((SERVER_DOMAIN, SERVER_PORT)) as sock:
        with context.wrap_socket(sock, server_hostname=SERVER_DOMAIN) as ssock:
            print(f"Connected to {SERVER_DOMAIN}:{SERVER_PORT}")
            try:
                response = ssock.recv(4096)
                print(response.decode())
            except ssl.SSLError as e:
                print(f"SSL error: {e}")

if __name__ == "__main__":
    main()
