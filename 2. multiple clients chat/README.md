## Multiple Clients Chat Application

This repository contains Python scripts for implementing a simple multiple clients chat application using socket programming. The application allows clients to connect to a central server, set usernames, send messages to each other, retrieve a list of connected users, and gracefully disconnect.

Files
chat_client_skeleton.py: Implements the chat client that connects to the server and interacts with other clients.
chat_server_skeleton.py: Implements the chat server that manages client connections, message routing, and user registration.
protocol.py: Defines constants and commands used by both the client and server for communication.
Technologies Used
Python 3.x
Socket Programming
Select Module (for multiplexing I/O)
Command-line Interface (CLI) interaction
Setup and Usage
Running the Server
Open a terminal.

Navigate to the directory containing chat_server_skeleton.py.

Run the server script:

bash
Copy code
python chat_server_skeleton.py
The server will start listening for incoming client connections on IP address 0.0.0.0 and port 7777.

Running the Client
Open another terminal for each client you want to simulate.

Navigate to the directory containing chat_client_skeleton.py.

Run the client script:

bash
Copy code
python chat_client_skeleton.py
Follow the on-screen instructions to set your username, send messages, retrieve connected users, and exit the chat.

Commands
NAME <name>: Set your username. The server will verify if the name is available.
GET_NAMES: Retrieve a list of all connected user names.
MSG <name> <message>: Send a message to a specific user.
EXIT: Disconnect from the chat and exit the client application.
Server Protocol Constants
SERVER_IP: IP address on which the server listens for incoming connections (default: 127.0.0.1).
SERVER_PORT: Port number used by the server (default: 7777).
MAX_MSG_LENGTH: Maximum length of messages exchanged between clients and the server (default: 1024 bytes).
Example Workflow
Clients connect to the server using socket connections.
Clients set their usernames using the NAME command.
Clients can send messages to other users using the MSG command.
Clients can retrieve a list of connected users using the GET_NAMES command.
Clients can gracefully disconnect using the EXIT command.
Notes
Ensure that the server is running and accessible from the clients' machines.
Adjust the server IP address and port in protocol.py if needed.
This is a basic implementation and may require enhancements for production-level usage, such as error handling and security measures.
License
This project is licensed under the MIT License.

Feel free to customize the paths, descriptions, and instructions based on your specific implementation and preferences. This template provides a structured approach to documenting your multiple clients chat application, making it easier for others to understand, use, and extend the functionality as needed.