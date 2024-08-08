### Multiple Client Chat - Client, Server, and Protocol

**Overview**

Multiple Clients Chat Application:

Built a chat application supporting multiple clients connecting to a central server.
Designed and implemented chat_client_skeleton.py and chat_server_skeleton.py for client-server communication.
Utilized a custom protocol defined in protocol.py to handle commands such as setting usernames, sending messages, and retrieving user lists.
Ensured asynchronous handling of client sessions for efficient real-time communication.

#### Chat Client

**Overview**

The `chat_client_skeleton.py` script provides a foundational implementation of a chat client designed to connect with a chat server using sockets. It facilitates bidirectional communication between users and the server, enabling command execution and message exchange.

**Features and Functionality**

**Socket Initialization and Connection:**
- **TCP Socket Initialization:** Initializes a TCP socket (`socket.socket(socket.AF_INET, socket.SOCK_STREAM)`) to establish a connection with the chat server. It utilizes constants `SERVER_IP` and `SERVER_PORT` from `chat_protocol_skeleton.py` for server address configuration.

**Command-Line Interface:**
- **Command Structure:** Upon connection, users interact with the client using the following commands:
  - **NAME <name>:** Sets the user's username, validated for uniqueness by the server.
  - **GET_NAMES:** Requests a list of all connected usernames from the server.
  - **MSG <name> <message>:** Sends a message to a specified user identified by `<name>`.
  - **EXIT:** Gracefully disconnects the client from the chat server.

**Sending and Receiving Messages:**
- **Message Handling Functions:**
  - **send_message(socket, message):** Encodes and sends UTF-8 encoded messages to the server.
  - **receive_message(socket):** Manages incoming messages from the server, handling `ConnectionResetError` gracefully by returning an empty string upon closed connections.

**Main Loop:**
- **Interactive Loop:** Within an infinite loop in `main()`, the client:
  - Monitors socket input asynchronously using `select.select()`.
  - Detects user keypresses using `msvcrt.kbhit()` (specifically on Windows), with `getch()` retrieving single characters.
  - Processes user commands, transmits them to the server, and displays corresponding server responses.
  - Safely exits the loop and closes the socket upon receiving the `EXIT` command.

**Code Structure and Design:**
- **Modular Design:** Segregates socket operations into `send_message()` and `receive_message()` functions, promoting code reusability and clarity.
- **User Interaction:** Provides clear command prompts and instructions, enhancing user experience and usability.
- **Error Handling:** Implements basic error handling for socket operations and connection issues, ensuring robustness in communication.

#### Chat Server

**Overview**

`chat_server_skeleton.py` functions as a foundational chat server implementation supporting multiple client connections via sockets. It manages various chat functionalities such as username assignment, user listing retrieval, message transmission, and client disconnection, facilitated by constants and commands defined in `chat_protocol_skeleton.py`.

**Features and Functionality**

**Server Initialization:**
- Initializes a TCP socket (`socket.socket(socket.AF_INET, socket.SOCK_STREAM)`) and binds it to `SERVER_IP` and `SERVER_PORT`. Listens for incoming client connections.

**Client Handling:**
- Utilizes `select.select()` for efficient asynchronous I/O handling, enabling concurrent management of multiple clients.

**Command Handling Functions:**
- **name_handle(parts, clients_names, current_socket):** Manages the `NAME` command to set a client's username, ensuring uniqueness.
- **get_name_handle(clients_names, current_socket):** Processes the `GET_NAMES` command to retrieve a list of all connected usernames.
- **msg_handle(parts, clients_names, current_socket):** Handles the `MSG` command to facilitate message exchange between clients, validating sender and recipient.
- **exit_handle(clients_names, current_socket):** Executes the `EXIT` command to disconnect a client from the chat.

**Client Management:**
- Tracks client connections using `client_sockets` and manages usernames via `clients_names` dictionary.
- Removes clients from these lists upon disconnection and appropriately closes associated sockets.

**Code Structure and Design:**
- **Modular Approach:** Segregates command handling into distinct functions (`handle_client_request()`, `name_handle()`, `get_name_handle()`, `msg_handle()`, `exit_handle()`), enhancing code clarity and separation of concerns.
- **Error Handling:** Incorporates basic error handling for socket operations and gracefully manages client disconnections.
- **Debugging Output:** Utilizes print statements for debugging purposes, providing visibility into client-server interactions and socket management.

#### Chat Protocol (chat_protocol_skeleton.py)

**Overview**

`chat_protocol_skeleton.py` defines essential constants and commands integral to the chat client-server communication, ensuring uniformity and ease of maintenance across implementations.

**Constants and Commands**

**Server Configuration:**
- **SERVER_IP and SERVER_PORT:** Specifies the IP address and port where the server binds to listen for incoming connections.
- **MAX_MSG_LENGTH:** Sets the maximum length of messages that clients can transmit to the server.

**Client-Server Commands:**
- **COMMAND_NAME, COMMAND_GET_NAMES, COMMAND_MSG, COMMAND_EXIT:** Represents distinct commands that clients can send to the server, facilitating user interactions such as username setting, user listing retrieval, message exchange, and client disconnection.

**Suggestions**

**Clarity and Consistency:** The constants and commands are clearly defined, crucial for maintaining a standardized communication protocol. Further documentation or inline comments could enhance understanding and facilitate future extensions or modifications of the protocol.

### Conclusion

Collectively, `chat_client_skeleton.py`, `chat_server_skeleton.py`, and `chat_protocol_skeleton.py` constitute a foundational framework for building a basic chat application using Python sockets. Their modular design, clear command structure, and robust error handling mechanisms exemplify fundamental principles in client-server communication. Enhancements in documentation, error management, and scalability considerations will further strengthen these scripts for developing more sophisticated and scalable chat systems in the future. Overall, they provide a solid starting point for implementing reliable and efficient chat applications while maintaining clarity and simplicity in design.

עבודה טובה, מספר הערות:

1. שים לב להגיש בזמן!

2. יש לטפל בהערות pep8

3. מודפס פעמיים ללקוח להכניס מידע בכל פעם, אחד לפני שהשרת עונה ואחד אחרי

4. הפונקציות של שליחת וקבלת מידע צריך להתנהל בפרוטוקול ולא רק קבועים...

5. אין אינדיקציה מספיק טובה ללקוח כשהוא מכניס הודעה לא תקינה מסיבה זו או אחרת

6. פעולת EXIT מקריסה את הלקוח וכך גם לגבי סגירה אלימה של לקוח