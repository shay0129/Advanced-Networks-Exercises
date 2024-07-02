# protocol.py
# Implement the missing functions in the protocol.py file. The functions are used to create a secure communication protocol between the client and the server. The protocol includes symmetric encryption, Diffie-Hellman key exchange, RSA key exchange, message integrity verification, and message authentication code (MAC) generation. The functions are used in the client.py and server.py files to establish a secure connection between the client and the server. The protocol.py file contains the following functions that need to be implemented:

import random


LENGTH_FIELD_SIZE = 2
PORT = 8820

# Diffie-Hellman parameters (public)
DIFFIE_HELLMAN_P = 65521 # A prime number
DIFFIE_HELLMAN_G = 3   # A primitive root modulo p

# Diffie-Hellman functions:
def diffie_hellman_choose_private_key():
    """Choose a 16-bit size private key"""
    return random.randint(1, DIFFIE_HELLMAN_P - 1)

def diffie_hellman_calc_public_key(private_key):
    """G**private_key mod P"""
    return pow(DIFFIE_HELLMAN_G, private_key, DIFFIE_HELLMAN_P)

def diffie_hellman_calc_shared_secret(other_side_public, my_private):
    """other_side_public**my_private mod P"""
    return pow(other_side_public, my_private, DIFFIE_HELLMAN_P)

def symmetric_encryption(input_data, key):
    """Return the encrypted / decrypted data using XOR method.
    The key is 16 bits. If the length of the input data is odd, use only the bottom 8 bits of the key."""
    encrypted = bytearray()
    for i in range(len(input_data)):
        encrypted.append(input_data[i] ^ (key & 0xFF if i % 2 == 0 else key >> 8))
    return encrypted

# RSA functions:
def generate_large_primes():
    return 61, 53

def get_RSA_private_key(p, q, e):
    totient = (p - 1) * (q - 1)
    d = pow(e, -1, totient)
    return d

def calc_signature(hash_value, private_key):
    d, n = private_key
    return pow(hash_value, d, n)

def create_msg(data):
    return f"{len(data):04d}:{data}"

def get_msg(sock):
    length = int(sock.recv(4).decode())
    data = sock.recv(length).decode()
    return length == len(data), data



def is_prime(num):
    """Check if a number is prime."""
    if num < 2:
        return False
    for i in range(2, int(num ** 0.5) + 1):
        if num % i == 0:
            return False
    return True
