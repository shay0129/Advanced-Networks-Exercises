# chat_client_skeleton.py - A simple chat client that connects to a chat server and sends messages

import socket
import select
import msvcrt
import chat_protocol_skeleton as protocol

def send_message(socket, message):
    '''Send a message to the socket.'''
    socket.send(message.encode())

def receive_message(socket):
    '''Receive a message from the socket and return it as a string. If the connection is closed, return an empty string.'''
    try:
        data = socket.recv(1024).decode()
        return data
    except ConnectionResetError:
        return ""

def main():
    # Initialize the socket
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.connect((protocol.SERVER_IP, protocol.SERVER_PORT))

    print("Welcome to the Chat Application!\n"
          "Available commands:\n"
          "1. NAME <name> - Set your username. Server will reply with an error if the name is duplicate.\n"
          "2. GET_NAMES - Get a list of all connected user names.\n"
          "3. MSG <name> <message> - Send a message to the specified user.\n"
          "4. EXIT - Disconnect from the chat.\n")

    print("Please enter commands\n", end='', flush=True)
    command = ""

    while True:
        read_sockets, _, _ = select.select([my_socket], [], [], 0.1)
        
        if msvcrt.kbhit(): # Check if a key was pressed
            ch = msvcrt.getch().decode() # Get a single character 
            if ch == '\r':  # Enter key
                if command == "EXIT":
                    send_message(my_socket, command)
                    break
                send_message(my_socket, command)
                command = ""
                print("\nPlease enter commands\n", end='', flush=True)
            else:
                print(ch, end="", flush=True)
                command += ch

        for sock in read_sockets: # Check if there is data to read from the server
            data = receive_message(sock)
            if data:
                print(f"\nServer sent:\t {data}\n")
                print("\nPlease enter commands\n", end='', flush=True)

    my_socket.close()

if __name__ == '__main__':
    main()
