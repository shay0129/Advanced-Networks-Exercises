## Python Networking Exercises

This repository contains a collection of Python networking exercises and projects focusing on various aspects of network communication and protocols.

Projects Overview
**Exercise 1: SMTP Client and Server**
Description:
Implementing a basic SMTP client-server interaction for sending emails using Python sockets.

Files:
SMTP_client.py: Client-side implementation for sending emails.
SMTP_server.py: Server-side implementation for receiving and processing emails.
SMTP_protocol.py: Defines constants and protocols used by the SMTP client and server.
Usage Instructions:
SMTP_server.py:

Run the server script to listen for incoming connections and handle SMTP commands.
Ensure Python 3.x is installed and execute:
```bash
python SMTP_server.py
```
SMTP_client.py:

Run the client script to connect to the server and send emails.
Adjust SERVER_NAME and other configurations as needed.
Execute the client script using:
```bash
python SMTP_client.py
```
**Exercise 2: Multiple Clients Chat Application**
Description:
Implementing a chat application where multiple clients can connect to a central server, set usernames, send messages to each other, and retrieve a list of connected users.

Files:
chat_client_skeleton.py: Client-side implementation for interacting with the chat server.
chat_server_skeleton.py: Server-side implementation for managing client connections and messages.
protocol.py: Defines constants and commands used by both the client and server.
Setup Instructions:
Server Setup:

Run the server script on a host machine:
```bash
python chat_server_skeleton.py
```
Ensure proper configuration of SERVER_IP and SERVER_PORT in protocol.py.
Client Setup:

Run the client script on each client machine:
bash
Copy code
python chat_client_skeleton.py
Follow the command-line prompts to set username, send messages, and interact with other clients.
Commands:
NAME <name>: Set username for chat.
GET_NAMES: Retrieve list of connected user names.
MSG <name> <message>: Send message to specified user.
EXIT: Disconnect from chat.