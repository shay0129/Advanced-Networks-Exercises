# SMTP_client.py - A simple SMTP client that sends an email using the SMTP protocol

import socket
import base64
import SMTP_protocol

CLIENT_NAME = "client.net"

EMAIL_TEXT = """
From: sender@example.com\r\n
To: recipient@example.com\r\n
Subject: Test Email\r\n
\r\n
This is a test email.
"""

def create_EHLO():
    return f"EHLO {CLIENT_NAME}\r\n".encode()

def create_AUTH_LOGIN_message():
    return "AUTH LOGIN\r\n".encode()

def create_USER_message(username):
    username_bytes = username.encode()
    return f"{base64.b64encode(username_bytes).decode()}\r\n".encode()

def create_PASSWORD_message(password):
    password_bytes = password.encode()
    return f"{base64.b64encode(password_bytes).decode()}\r\n".encode()

def create_MAIL_FROM_message(sender_email):
    return f"MAIL FROM: <{sender_email}>\r\n".encode()

def create_RCPT_TO_message(recipient_email):
    return f"RCPT TO: <{recipient_email}>\r\n".encode()

def create_DATA_message():
    return "DATA\r\n".encode()

def create_QUIT_message():
    return "QUIT\r\n".encode()

def main():
    SERVER_NAME = "smtp.example.com"
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.connect(('127.0.0.1', SMTP_protocol.PORT))

    try:
        response = my_socket.recv(1024).decode()
        print(response)
        if not response.startswith(SMTP_protocol.SMTP_SERVICE_READY):
            print("Error connecting to server")
            return

        my_socket.send(create_EHLO()) # send EHLO command to server
        response = my_socket.recv(1024).decode() # get Hello's server
        print(response)
        if not response.startswith(SMTP_protocol.REQUESTED_ACTION_COMPLETED):
            print("Error sending EHLO")
            return

        my_socket.send(create_AUTH_LOGIN_message()) # send AUTH LOGIN command to server
        response = my_socket.recv(1024).decode()
        print(response)
        if not response.startswith(SMTP_protocol.AUTH_INPUT):
            print("Error starting authentication")
            return

        username = "barbie"
        my_socket.send(create_USER_message(username)) # Send Client's username
        response = my_socket.recv(1024).decode()
        print(response)
        if not response.startswith(SMTP_protocol.REQUESTED_ACTION_COMPLETED):
            print("Error sending username")
            return

        password = "helloken"
        my_socket.send(create_PASSWORD_message(password)) # Send Client's password
        response = my_socket.recv(1024).decode()
        print(response)
        if not response.startswith(SMTP_protocol.AUTH_SUCCESS):
            print("Error sending password")
            return

        sender_email = "sender@example.com"
        my_socket.send(create_MAIL_FROM_message(sender_email))
        response = my_socket.recv(1024).decode()
        print(response)
        if not response.startswith(SMTP_protocol.REQUESTED_ACTION_COMPLETED):
            print("Error sending MAIL FROM")
            return

        recipient_email = "recipient@example.com"
        my_socket.send(create_RCPT_TO_message(recipient_email))
        response = my_socket.recv(1024).decode()
        print(response)
        if not response.startswith(SMTP_protocol.REQUESTED_ACTION_COMPLETED):
            print("Error sending RCPT TO")
            return

        my_socket.send(create_DATA_message())
        response = my_socket.recv(1024).decode()
        print(response)
        if not response.startswith(SMTP_protocol.ENTER_MESSAGE):
            print("Error starting DATA")
            return

        my_socket.send(f"{EMAIL_TEXT}\r\n.\r\n".encode())
        response = my_socket.recv(1024).decode()
        print(response)
        if response.startswith(SMTP_protocol.REQUESTED_ACTION_COMPLETED):
            print("Email sent successfully!")
        else:
            print("Error sending email:", response)

        my_socket.send(create_QUIT_message())
        response = my_socket.recv(1024).decode()
        print(response)

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        print("Closing connection")
        my_socket.close()

if __name__ == "__main__":
    main()
