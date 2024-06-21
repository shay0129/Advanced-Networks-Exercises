## SMTP Exercise Solutions

This repository contains Python scripts for implementing a basic SMTP (Simple Mail Transfer Protocol) client-server interaction. The scripts simulate sending an email from a client to a server using socket programming and adhere to SMTP protocol standards.

Files
SMTP_client.py: Implements the SMTP client that sends an email to the server.
SMTP_server.py: Implements the SMTP server that receives emails from clients.
SMTP_protocol.py: Defines constants and protocols used by both the client and server.
Technologies Used
Python 3.x
Socket Programming
Base64 Encoding
Setup and Usage
Running the SMTP Server
Open a terminal.

Navigate to the directory containing SMTP_server.py.

Run the server script:

bash
Copy code
python SMTP_server.py
The server will start listening for incoming connections on port 25 (SMTP default).

Running the SMTP Client
Open another terminal.

Navigate to the directory containing SMTP_client.py.

Run the client script:

bash
Copy code
python SMTP_client.py
Ensure the client script is configured with the appropriate server address (SERVER_NAME) and port (default SMTP port).

Sending an Email
The client script (SMTP_client.py) sends a test email to demonstrate the interaction.
Modify the EMAIL_TEXT variable in SMTP_client.py to customize the email content.
The server (SMTP_server.py) simulates the receipt of the email, validating commands and responses according to SMTP protocol standards.
SMTP Protocol Constants
SMTP_service_ready (220): Initial server response indicating readiness.
Requested_action_completed (250): Successful response to commands.
Command_syntax_error (500): Error response for unrecognized commands.
Incorrect_auth (535): Authentication failure response.
Enter_message (354): Response to indicate data (email content) acceptance.
Auth_input (334): Prompt for username during authentication.
Auth_success (235): Successful authentication response.
Goodbye (221): Closing connection response.
Example Workflow
The client initiates communication with the server (EHLO, AUTH LOGIN).
Authentication details (username and password) are exchanged securely using base64 encoding.
The client sends email metadata (MAIL FROM, RCPT TO).
The client sends the email content (DATA) and terminates with ..
Upon successful receipt, the server acknowledges with appropriate responses.
Notes
Ensure proper firewall settings allow communication over SMTP port (default 25).
Adjust script variables (CLIENT_NAME, SERVER_NAME, EMAIL_TEXT, user_names) to match your environment and test scenarios.
License
This project is licensed under the MIT License.

Adjust the paths, descriptions, and instructions as per your actual setup and preferences. This template provides a clear and structured approach to documenting your SMTP exercise solutions, making it easier for others to understand, use, and modify them as needed.





