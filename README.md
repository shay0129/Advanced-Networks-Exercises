### Python Networking Exercises

This repository contains a collection of Python networking exercises and projects focusing on various aspects of network communication and protocols.

## Projects Overview

### Exercise 1: SMTP Client and Server

**Description:**
Implementing a basic SMTP client-server interaction for sending emails using Python sockets.

**Files:**
- `SMTP_client.py`: Client-side implementation for sending emails.
- `SMTP_server.py`: Server-side implementation for receiving and processing emails.
- `SMTP_protocol.py`: Defines constants and protocols used by the SMTP client and server.

**Usage Instructions:**

#### SMTP Server

Run the server script to listen for incoming connections and handle SMTP commands.

1. Ensure Python 3.x is installed.
2. Execute the server script:
   ```bash
   python SMTP_server.py
   ```

#### SMTP Client

Run the client script to connect to the server and send emails. Adjust `SERVER_NAME` and other configurations as needed.

1. Execute the client script:
   ```bash
   python SMTP_client.py
   ```

### Exercise 2: Multiple Clients Chat Application

**Description:**
Implementing a chat application where multiple clients can connect to a central server, set usernames, send messages to each other, and retrieve a list of connected users.

**Files:**
- `chat_client_skeleton.py`: Client-side implementation for interacting with the chat server.
- `chat_server_skeleton.py`: Server-side implementation for managing client connections and messages.
- `protocol.py`: Defines constants and commands used by both the client and server.

**Setup Instructions:**

#### Server Setup

Run the server script on a host machine:

1. Ensure proper configuration of `SERVER_IP` and `SERVER_PORT` in `protocol.py`.
2. Execute the server script:
   ```bash
   python chat_server_skeleton.py
   ```

#### Client Setup

Run the client script on each client machine:

1. Execute the client script:
   ```bash
   python chat_client_skeleton.py
   ```
2. Follow the command-line prompts to set username, send messages, and interact with other clients.

**Commands:**
- `NAME <name>`: Set username for chat.
- `GET_NAMES`: Retrieve list of connected user names.
- `MSG <name> <message>`: Send message to specified user.
- `EXIT`: Disconnect from chat.

### Exercise 2: Multiple Clients Chat Application
//

//

//

//

//

### Exercise 4: DNS Enumeration

**Description:**
Implementing a DNS enumeration tool to retrieve DNS records for a given domain using Python.

**Files:**
- `dns_enumeration.py`: Implementation for performing DNS enumeration.

**Usage Instructions:**

1. Ensure Python 3.x is installed.
2. Execute the DNS enumeration script:
   ```bash
   python dns_enumeration.py <domain>
   ```
   Replace `<domain>` with the domain name you want to enumerate.

**Example:**

To enumerate DNS records for `example.com`:
```bash
python dns_enumeration.py example.com
```

### Exercise 5: HTTP Server

**Description:**
Implementing a basic HTTP server to handle GET and POST requests.

**Files:**
- `http_server.py`: Implementation of a simple HTTP server.

**Usage Instructions:**

1. Ensure Python 3.x is installed.
2. Execute the HTTP server script:
   ```bash
   python http_server.py
   ```
3. Access the server using a web browser or a tool like `curl`:
   - For a GET request:
     ```bash
     curl http://localhost:8080
     ```
   - For a POST request:
     ```bash
     curl -X POST -d "param1=value1&param2=value2" http://localhost:8080
     ```

## Summary

This repository includes exercises for implementing SMTP client-server communication, a multiple clients chat application, a DNS enumeration tool, and a basic HTTP server. Each exercise demonstrates fundamental networking concepts using Python, providing a practical approach to understanding network protocols and communication.