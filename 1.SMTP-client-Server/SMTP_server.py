# SMTP_server.py - A simple SMTP server that requires authentication to send emails

import socket
import base64
import SMTP_protocol

IP = "0.0.0.0"
SOCKET_TIMEOUT = 1

SERVER_NAME = "SMTP_server.com"
user_names = {"shooki": "abcd1234", "barbie": "helloken"}

def create_initial_response():
    return f"{SMTP_protocol.SMTP_SERVICE_READY} Server ready\r\n".encode()

def create_EHLO_response(client_message):
    if not client_message.startswith("EHLO"):
        return f"{SMTP_protocol.COMMAND_SYNTAX_ERROR}\r\n".encode()
    client_name = client_message.split()[1]
    return f"{SMTP_protocol.REQUESTED_ACTION_COMPLETED}-{SERVER_NAME} Hello {client_name}\r\n".encode()

def create_AUTH_LOGIN_response():
    return f"{SMTP_protocol.AUTH_INPUT} Username:\r\n".encode()

def create_USER_response(username):
    if username not in user_names:
        return f"{SMTP_protocol.INCORRECT_AUTH}\r\n".encode()
    return f"{SMTP_protocol.REQUESTED_ACTION_COMPLETED} User {username} authenticated\r\n".encode()

def create_PASSWORD_response(username, password):
    if user_names[username] != password:
        return f"{SMTP_protocol.INCORRECT_AUTH}\r\n".encode()
    return f"{SMTP_protocol.AUTH_SUCCESS} Authentication successful\r\n".encode()

def handle_MAIL_FROM(message):
    return f"{SMTP_protocol.REQUESTED_ACTION_COMPLETED} MAIL FROM accepted\r\n".encode()

def handle_RCPT_TO(message):
    return f"{SMTP_protocol.REQUESTED_ACTION_COMPLETED} RCPT TO accepted\r\n".encode()

def handle_DATA(message, client_socket):
    client_socket.send(f"{SMTP_protocol.ENTER_MESSAGE} End data with <CR><LF>.<CR><LF>\r\n".encode())
    data = client_socket.recv(1024).decode()
    return f"{SMTP_protocol.REQUESTED_ACTION_COMPLETED} Message accepted for delivery\r\n".encode()

def create_QUIT_response():
    return f"{SMTP_protocol.GOODBYE} Server closing connection\r\n".encode()

def handle_SMTP_client(client_socket):
    try:
        client_socket.send(create_initial_response())

        authenticated = False
        username = None

        while True:
            try:
                message = client_socket.recv(1024).decode().strip()
                print(f"Client message: {message}")
# EHLO
                if message.startswith("EHLO"):
                    response = create_EHLO_response(message) # answer to client's EHLO command
                    client_socket.send(response)
                    if not response.decode().startswith(SMTP_protocol.REQUESTED_ACTION_COMPLETED):
                        return
# AUTH LOGIN
                elif message.startswith("AUTH LOGIN"):
                    client_socket.send(create_AUTH_LOGIN_response()) # Answer to Client's AUTH LOGIN command

                    username_message = client_socket.recv(1024).decode().strip()
                    print(f"Username base64 message: {username_message}") # YmFyYmll
                    username = base64.b64decode(username_message).decode().strip() # Translate Client's string in b64
                    print(f"Username: {username}") # barbie
                    response = create_USER_response(username) # Accept User's login
                    client_socket.send(response)

                    if not response.decode().startswith(SMTP_protocol.REQUESTED_ACTION_COMPLETED):
                        continue

                    password_message = client_socket.recv(1024).decode().strip()
                    print(f"Decoded password base64 message: {password_message}")
                    password = base64.b64decode(password_message).decode().strip()
                    print(f"Decoded password: {password}")
                    response = create_PASSWORD_response(username, password)
                    client_socket.send(response)

                    if response.decode().startswith(SMTP_protocol.AUTH_SUCCESS):
                        authenticated = True
                    else:
                        continue
# MAIL FROM
                elif authenticated:
                    if message.startswith("MAIL FROM"):
                        response = handle_MAIL_FROM(message)
                        client_socket.send(response)
# RCPT TO
                    elif message.startswith("RCPT TO"):
                        response = handle_RCPT_TO(message)
                        client_socket.send(response)
# DATA
                    elif message.startswith("DATA"):
                        response = handle_DATA(message, client_socket)
                        client_socket.send(response)
# QUIT
                    elif message.startswith("QUIT"):
                        response = create_QUIT_response()
                        client_socket.send(response)
                        break
                    else:
                        response = f"{SMTP_protocol.COMMAND_SYNTAX_ERROR} Invalid command\r\n".encode()
                        client_socket.send(response)
                else:
                    response = f"{SMTP_protocol.AUTH_REQUIRED} Authentication required\r\n".encode()
                    client_socket.send(response)
            except socket.timeout:
                print("Socket timeout occurred")
                break
            except ConnectionAbortedError:
                print("Connection aborted by client")
                break
            except Exception as e:
                print(f"An error occurred: {e}")
                break

    finally:
        client_socket.close()
        print("Connection closed")

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((IP, SMTP_protocol.PORT))
    server_socket.listen()
    print(f"Listening for connections on port {SMTP_protocol.PORT}")

    while True:
        client_socket, client_address = server_socket.accept()
        print('New connection received')
        client_socket.settimeout(SOCKET_TIMEOUT)
        handle_SMTP_client(client_socket)
        print("Connection closed")

if __name__ == "__main__":
    main()
