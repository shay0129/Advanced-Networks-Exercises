import socket

HOST = '127.0.0.1'
PORT = 65432

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))

    try:
        # Receive the encryption key from the server
        encryption_key = client_socket.recv(1024).decode()
        print(f"Received encryption key: {encryption_key}")

        # Request the resource
        client_socket.sendall(b"GET RESOURCE")

        while True:
            try:
                response = client_socket.recv(1024)
                if response:
                    if response == b"200 OK":
                        # Receive the resource data
                        resource_data = b""
                        while True:
                            part = client_socket.recv(1024)
                            if not part:
                                break
                            resource_data += part
                        if resource_data:
                            # Save the resource to a file
                            with open('resource.png', 'wb') as f:
                                f.write(resource_data)
                            print("Resource received and saved.")
                        break
                    
                    #if response == b"400 Bad Request":
                        #print("No certified clients available.")
                        #break

                    else:
                        print(f"Unexpected response: {response}")
                        break
            except Exception as e:
                print(f"Error while receiving data: {e}")
                break
    except Exception as e:
        print(f"Error while connecting or receiving data: {e}")

    client_socket.close()

if __name__ == "__main__":
    main()
