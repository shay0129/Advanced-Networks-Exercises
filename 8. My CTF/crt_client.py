import ssl
import socket

HOST = '127.0.0.1'
PORT = 65432

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    context = ssl.create_default_context()
    context.load_cert_chain(certfile='client.crt', keyfile='client.key')
    client_socket = context.wrap_socket(client_socket, server_hostname='localhost')
    
    client_socket.connect((HOST, PORT))

    encryption_key = client_socket.recv(1024).decode()
    print(f"Received encryption key: {encryption_key}")

    client_socket.sendall(b"GET RESOURCE")

    while True:
        try:
            response = client_socket.recv(1024)
            if response:
                print(f"Received: {response}")
                if response == b"resource.png":
                    with open('resource.png', 'wb') as f:
                        f.write(client_socket.recv(1024))
                    print("Resource received and saved.")
                    break
            else:
                break
        except Exception as e:
            print(f"Error: {e}")
            break

    client_socket.close()

if __name__ == "__main__":
    main()
