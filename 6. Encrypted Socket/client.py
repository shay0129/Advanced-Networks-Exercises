# client.py
# Implementing a client that communicates with a server using a secure connection
import socket
import protocol

def main():
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.connect(("127.0.0.1", protocol.PORT))

    # Diffie-Hellman Key Exchange
    # 1 - Choose private key
    client_private_key = protocol.diffie_hellman_choose_private_key()
    # 2 - Calculate public key
    client_public_key = protocol.diffie_hellman_calc_public_key(client_private_key)

    # 3 - Interact with server and calculate shared secret
    server_public_key = int(my_socket.recv(1024).decode())  # Receive server's public key
    my_socket.send(str(client_public_key).encode())  # Send client's public key to the server
    shared_secret = protocol.diffie_hellman_calc_shared_secret(server_public_key, client_private_key)
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
    
    # Exchange RSA public keys with server
    client_public_key = (e, n)
    my_socket.send(f"{client_public_key[0]},{client_public_key[1]}".encode())  # Send public key to server
    server_public_key = my_socket.recv(1024).decode().split(',')
    e_server, n_server = int(server_public_key[0]), int(server_public_key[1])

    rsa_public_key_server = {'e': e_server, 'n': n_server}
    rsa_private_key = {'d': d, 'n': n}

    while True:
        user_input = input("Enter command\n")
        # Add MAC (signature)
        # 1 - Calculate hash of user input
        calculated_hash = protocol.calc_hash(user_input)
        
        # 2 - Calculate the signature
        signature = protocol.calc_signature(calculated_hash, rsa_private_key)
        # Encrypt
        # Apply symmetric encryption to the user's input
        user_input_bytes = user_input.encode()  # Convert the user input to bytes
        encrypted_input = protocol.symmetric_encryption(user_input_bytes, symmetric_key)

        # Create a message to send to the server
        # Combine encrypted user's message with MAC
        msg = f"{encrypted_input.decode(errors='ignore')}:{signature}"
        # Send the message
        my_socket.send(protocol.create_msg(msg).encode())

        if user_input == 'EXIT':
            break

        # Receive server's message
        valid_msg, received_data = protocol.get_msg(my_socket)
        if not valid_msg:
            print("Something went wrong with the length field")
            continue

        # Check if server's message is authentic
        # 1 - Separate the message and the MAC
        message, received_mac = received_data.split(':')
        # 2 - Decrypt the message
        decrypted_message = protocol.symmetric_encryption(message.encode(), symmetric_key)
        # 3 - Calculate hash of the decrypted message
        message_hash = protocol.calc_hash(decrypted_message.decode(errors='ignore'))
        # 4 - Use server's public RSA key to decrypt the MAC and get the hash
        decrypted_mac = pow(int(received_mac), rsa_public_key_server['e'], rsa_public_key_server['n'])
        # 5 - Check if both calculations end up with the same result
        if message_hash == decrypted_mac:
            print("Message is authentic.")
        else:
            print("Message authenticity failed.")
        
        # Print server's message
        print(f"Server says: {decrypted_message.decode(errors='ignore')}")
        
        if decrypted_message.decode(errors='ignore') == 'EXIT':
            break

if __name__ == "__main__":
    main()
