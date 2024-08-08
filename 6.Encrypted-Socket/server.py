# server.py
# Encrypted socket server implementation


import socket
import protocol

def create_server_rsp(cmd):
    """Based on the command, create a proper response"""
    return f"Server response to {cmd}"

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", protocol.PORT))
    server_socket.listen()
    print("Server is up and running")
    client_socket, client_address = server_socket.accept()
    print("Client connected")

    # Diffie-Hellman Key Exchange
    # 1 - Choose private key
    server_private_key = protocol.diffie_hellman_choose_private_key()
    # 2 - Calculate public key
    server_public_key = protocol.diffie_hellman_calc_public_key(server_private_key)

    # 3 - Interact with client and calculate shared secret
    # Send server's public key to the client
    client_socket.send(str(server_public_key).encode())

    # Receive client's public key
    client_public_key = int(client_socket.recv(1024).decode())

    # Calculate the shared secret
    shared_secret = protocol.diffie_hellman_calc_shared_secret(client_public_key, server_private_key)
    print(f"Shared secret: {shared_secret}")

    # Derive the symmetric key from the shared secret
    symmetric_key = shared_secret & 0xFFFF

    # RSA Key Exchange
    # Pick public key
    e = 65537
    # Calculate matching private key
    p, q = protocol.generate_large_primes()
    n = p * q  # Compute the modulus
    d = protocol.get_RSA_private_key(p, q, e)  # Calculate the private key such that (d * e) % totient == 1

    # Exchange RSA public keys with client
    server_public_key = (e, n)
    client_socket.send(f"{server_public_key[0]},{server_public_key[1]}".encode())  # Send public key to client
    client_public_key = client_socket.recv(1024).decode().split(',')
    e_client, n_client = int(client_public_key[0]), int(client_public_key[1])

    rsa_public_key_client = {'e': e_client, 'n': n_client}
    rsa_private_key = {'d': d, 'n': n}

    while True:
        # Receive client's message
        valid_msg, received_data = protocol.get_msg(client_socket)
        if not valid_msg:
            print("Something went wrong with the length field")
            continue

        if received_data == "EXIT":
            break

        # Separate the message and the MAC
        encrypted_message, received_mac = received_data.split(':')

        # Decrypt the message
        decrypted_message = protocol.symmetric_encryption(encrypted_message.encode(), symmetric_key).decode()

        # Create response
        response = create_server_rsp(decrypted_message)
        
        # Add MAC (signature) to the response
        response_hash = protocol.calc_hash(response)
        response_mac = protocol.calc_signature(response_hash, rsa_private_key)
        response_mac_str = str(response_mac)

        # Encrypt the response
        encrypted_response = protocol.symmetric_encryption(response.encode(), symmetric_key)
        # Combine encrypted response with MAC
        response_msg = f"{encrypted_response.decode(errors='ignore')}:{response_mac_str}"
        # Send to client
        client_socket.send(protocol.create_msg(response_msg).encode())

    print("Closing\n")
    client_socket.close()
    server_socket.close()

if __name__ == "__main__":
    main()
