HTTP Server Implementation
This project implements a simple HTTP server in Python, capable of serving static files and handling basic HTTP requests. It includes functionality for handling various HTTP status codes, serving static files (HTML, CSS, JavaScript, images), and managing client connections.

Table of Contents
Features
Installation
Usage
Tests
Contributing
License
Features
Static File Serving: The server can serve HTML, CSS, JavaScript, images (JPG, JPEG, PNG, GIF), and other static files from a designated web root directory.
HTTP Status Codes: Supports common HTTP status codes (200 OK, 302 Found, 404 Not Found, 500 Internal Server Error, 403 Forbidden).
Redirection Handling: Implements redirection based on a predefined dictionary of redirects.
Client Request Handling: Handles incoming HTTP requests using socket programming, including validation and appropriate response generation.
Server Stability: Demonstrates stability under multiple client connections and manages socket timeouts gracefully.
Installation
Clone the repository:

bash
Copy code
git clone https://github.com/your/repository.git
cd HTTP_Server
Install dependencies:

Ensure you have Python 3.x installed. Dependencies such as requests for testing purposes should be installed via pip:

bash
Copy code
pip install requests
Run the server:

Start the server by running HTTP_server_shell.py. Ensure it is configured with appropriate IP address, port, and resource folder.

bash
Copy code
python HTTP_server_shell.py
Usage
Configure the server parameters in HTTP_server_shell.py such as IP address, port, socket timeout, and resource folder (webroot).
Ensure your web content (HTML files, CSS files, JavaScript files, images) is placed in the webroot directory.
Access the server from a web browser using http://localhost:80 (adjust the IP and port as per your configuration).
Tests
This project includes automated tests to verify the functionality of the HTTP server. The tests cover basic functionality, error handling, server stability, and more. To run the tests:

bash
Copy code
python tests.py
Basic Functionality Test: Checks if the server loads all resources correctly.
302 Redirect Test: Verifies the server's handling of 302 redirects.
404 Not Found Test: Ensures the server correctly returns 404 errors for non-existent resources.
Server Stability Test: Tests the server's stability under multiple client connections and refresh scenarios.
Contributing
Contributions are welcome! If you find any issues or have suggestions for improvement, please open an issue or submit a pull request.

License
This project is licensed under the MIT License.








Support for POST Requests: Extend the server to handle not just GET requests but also POST requests. This would involve parsing incoming POST data and responding accordingly.

Persistent Connections (HTTP Keep-Alive): Implement support for persistent connections to improve performance by allowing multiple requests and responses to be sent over a single TCP connection.

Content-Length Handling: Ensure proper handling of Content-Length headers for both incoming requests and outgoing responses. This is crucial for correctly reading and sending data when dealing with file transfers or POST requests.

MIME Type Detection: Enhance the server to detect MIME types based on file extensions or content inspection rather than relying solely on file extensions.

Error Logging: Implement logging to record various events such as client connections, requests received, responses sent, and any errors encountered. This could provide valuable insights for debugging and monitoring the server's activity.

Concurrency: Explore ways to handle multiple client connections concurrently using threading or asynchronous I/O, improving the server's responsiveness to multiple clients.

Security Features: Integrate basic security measures such as input validation, preventing directory traversal attacks, and ensuring proper handling of special characters in URLs.

Configuration File: Create a simple configuration file (e.g., JSON or YAML) to store settings such as IP address, port number, default URLs, and redirection rules. This can make the server more configurable without hardcoding values in the code.

Enhanced Error Responses: Customize error responses (e.g., 403 Forbidden, 405 Method Not Allowed) to provide more informative messages or instructions to clients.

Caching Mechanism: Implement a basic caching mechanism to store frequently accessed resources in memory, reducing file I/O and improving response times for repetitive requests.