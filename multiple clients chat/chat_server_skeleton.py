import socket
import select
import protocol

SERVER_IP = "0.0.0.0"

def name_handle(parts, clients_names, current_socket):
    '''Handle the name command and return the reply and the current socket as the destination socket.'''
    if len(parts) < 2:
        return "Invalid NAME command format", current_socket
    else:
        requested_name = parts[1].strip()
        if requested_name in clients_names:  # Check if the name is already taken
            return f"Error: Name '{requested_name}' is already taken.", current_socket
        else:
            # Remove any previous registration of the current socket
            for name, sock in list(clients_names.items()):
                if sock == current_socket:
                    del clients_names[name]
            clients_names[requested_name] = current_socket
            return f"HELLO {requested_name}!", current_socket

            
def get_name_handle(clients_names, current_socket):
    '''Handle the get_names command and return the reply and the current socket as the destination socket.'''
    if clients_names:
        return ", ".join(clients_names.keys()), current_socket
    else:
        return " ", current_socket  # Return space if no clients are registered and the current socket as the destination socket

def msg_handle(parts, clients_names, current_socket):
    '''Handle the msg command and return the reply and destination socket.'''
    if len(parts) < 3:
        return "Invalid MSG command format", None
    
    recipient_name = parts[1].strip() # Extract the recipient name
    message = parts[2].strip() # Extract the message
    sender_name = next((name for name, sock in clients_names.items() if sock == current_socket), None)

    if sender_name is None:
        return "Error: Sender not registered.", None
    elif recipient_name == sender_name: # Check if the sender is the recipient
        return "Error: You cannot send a message to yourself.", None
    elif sender_name in clients_names and recipient_name in clients_names: # Check if the recipient exists
        dest_socket = clients_names.get(recipient_name)
        if dest_socket == current_socket:
            return "", None  # Clear reply if sender is the same as the recipient
        return f"{sender_name} sent {message}", dest_socket
    else: # Return an error if the recipient does not exist
        return f"Error: User '{recipient_name}' does not exist.", None


def exit_handle(clients_names, current_socket):
    '''Handle the exit command and return the reply.'''
    for name, sock in list(clients_names.items()):
            if sock == current_socket: # Remove the client from the list of clients
                del clients_names[name]
    current_socket.close()
    return "Goodbye!"

def handle_client_request(current_socket, clients_names, data):
    """Handle the client request and return the reply and destination socket."""
    response = None
    dest_socket = None

    parts = data.split(maxsplit=2)
    if not parts:
        return "", None  # Return empty reply and None destination socket

    command = parts[0].strip()
    if command == protocol.COMMAND_NAME:
        response, dest_socket = name_handle(parts, clients_names, current_socket)
        print(f"Response from name_handle: {response}")  # Debugging statement

    elif command == protocol.COMMAND_GET_NAMES:
        response, dest_socket = get_name_handle(clients_names, current_socket)

    elif command == protocol.COMMAND_MSG:
        response, dest_socket = msg_handle(parts, clients_names, current_socket)

    elif command == protocol.COMMAND_EXIT:
        response, dest_socket = exit_handle(clients_names, current_socket)
    else:
        response = f"Unknown command: {command}"
    if response is None:
        response = ""  # Set reply to empty string if not already set

    return response, dest_socket # Return the reply and destination socket

def print_client_sockets(client_sockets):
    for c in client_sockets:
        print("\t", c.getpeername())


def main():
    print("Setting up server...")
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_IP, protocol.SERVER_PORT))
    server_socket.listen()
    print("Listening for clients...")
    client_sockets = []
    messages_to_send = []
    clients_names = {}
    while True:
        read_list = client_sockets + [server_socket]
        ready_to_read, ready_to_write, in_error = select.select(read_list, client_sockets, [])
        for current_socket in ready_to_read:
            if current_socket is server_socket:
                client_socket, client_address = server_socket.accept()
                print("Client joined!\n", client_address)
                client_sockets.append(client_socket)
                print_client_sockets(client_sockets)
            else:
                print("Data from client\n")
                data = current_socket.recv(protocol.MAX_MSG_LENGTH).decode()
                if data == "":
                    print("Connection closed\n")
                    for entry in clients_names.keys():
                        if clients_names[entry] == current_socket:
                            sender_name = entry
                    clients_names.pop(sender_name)
                    client_sockets.remove(current_socket)
                    current_socket.close()
                else:
                    print(data)
                    (response, dest_socket) = handle_client_request(current_socket, clients_names, data)
                    messages_to_send.append((dest_socket, response))

        # write to everyone (note: only ones which are free to read...)
        for message in messages_to_send:
            current_socket, data = message
            if current_socket in ready_to_write:
                current_socket.send(data.encode())
                messages_to_send.remove(message)



if __name__ == '__main__':
    main()
