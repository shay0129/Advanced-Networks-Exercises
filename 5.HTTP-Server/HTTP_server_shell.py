# HTTP_server_shell.py
# This file contains the main server logic for the HTTP server implementation.
import os
import socket
import urllib.parse
import functools # 
import HTTP_protocol as protocol

# Constants for the server
IP = '0.0.0.0'
PORT = 80
SOCKET_TIMEOUT = 0.5

# Constants for the HTTP server
RESOURCE_FOLDER = 'webroot'
REDIRECTION_DICT = {
    '/doremon': 'css/doremon.css',
    '/abstract': 'imgs/abstract.jpg',
    '/favicon': 'imgs/favicon.ico',
    '/loading': 'imgs/loading.gif',
    '/index': 'index.html',
    '/box': 'js/box.js',
    '/jquery': 'jquery.min.js',
    '/submit': 'js/submit.js',
    '/': 'index.html'  # Default url
}

def get_file_data(filename):
    """ Get data from file """
    try:
        with open(filename, 'rb') as file:
            print(f"Serving file: {filename}")
            return file.read()
    except FileNotFoundError:
        print(f"File not found: {filename}")
        return None
    except IOError as e:
        print(f"IOError: Failed to read file {filename}: {e}")
        return None
    except Exception as e:
        print(f"Error reading file {filename}: {e}")
        return None

def validate_and_calculate(query_params, operation):
    """
    Validates parameters and performs a calculation.

    Args:
        query_params (dict): Query parameters.
        operation (str): Type of calculation.

    Returns:
        tuple: (status code, content type, response content).
    """

    required_params = {
        "calculate_area": ["height", "width"],
        "calculate_next": ["num"]
    }

    missing_params = set(required_params[operation]) - set(query_params.keys())
    if missing_params:
        error_message = f"Missing parameters: {', '.join(missing_params)}"
        return 400, 'text/plain', error_message.encode()

    try:
        if operation == "calculate_area":
            height = float(query_params['height'][0])
            width = float(query_params['width'][0])
            area = 0.5 * height * width
            response_content = f"Area calculated for height={height} and width={width}: {area}"
        elif operation == "calculate_next":
            num = int(query_params['num'][0])
            response_content = str(num + 1)
        else:
            raise ValueError(f"Invalid operation: {operation}")
    except (ValueError, KeyError) as e:
        error_message = f"Invalid parameters for {operation}: {e}"
        return 400, 'text/plain', error_message.encode()

    return 200, 'text/plain', response_content.encode()

# Use functools.partial to create specific handlers
handle_calculate_area = functools.partial(validate_and_calculate, operation="calculate_area")
handle_calculate_next = functools.partial(validate_and_calculate, operation="calculate_next")

def serve_client_request(resource, request_data, client_socket):
    """ Serve client requests based on the resource """
    try:
        # Parse the resource to handle query parameters
        parsed_url = urllib.parse.urlparse(resource)
        path = parsed_url.path
        query_params = urllib.parse.parse_qs(parsed_url.query)

        if path in REDIRECTION_DICT:
            new_location = REDIRECTION_DICT[path]
            print(f"Redirecting {path} to {new_location}")
            client_socket.send(protocol.generate_status_code(302, location=new_location))
        elif path == '/calculate-area':
            status_code, content_type, response_content = handle_calculate_area(query_params)
            client_socket.send(protocol.generate_status_code(status_code, content_type, response_content))
        elif path == '/calculate-next':
            status_code, content_type, response_content = handle_calculate_next(query_params)
            client_socket.send(protocol.generate_status_code(status_code, content_type, response_content))
        else:
            # Serve static files from RESOURCE_FOLDER
            normalized_resource = os.path.normpath(path.lstrip('/'))
            requested_file = os.path.join(RESOURCE_FOLDER, normalized_resource)
            data = get_file_data(requested_file)

            if data is not None:
                filetype = path.split('.')[-1] if '.' in path else 'html'
                client_socket.send(protocol.generate_status_code(200, protocol.get_content_type(filetype), data))
            else:
                client_socket.send(protocol.generate_status_code(404, 'text/plain'))

    except Exception as e:
        print(f"Exception occurred while handling request: {e}")
        client_socket.send(protocol.generate_status_code(500, 'text/plain'))

    finally:
        client_socket.close()

def handle_client(client_socket):
    """ Handle client connections """
    try:
        client_socket.settimeout(SOCKET_TIMEOUT)
        request_data = client_socket.recv(1024)
        request_text = request_data.decode()
        valid_request, resource = protocol.validate_http_request(request_text)
        if valid_request:
            serve_client_request(resource, request_data, client_socket)
        else:
            client_socket.send(protocol.generate_status_code(404, 'text/plain'))
    except socket.timeout:
        print("Socket timed out while waiting for data")
    except ConnectionResetError:
        print("Client closed the connection unexpectedly")
    except Exception as e:
        print(f"Error handling client request: {e}")
    finally:
        client_socket.close()



def main():
    import signal
    # Setup signal handler for Ctrl+C
    signal.signal(signal.SIGINT, handle_interrupt)
    """ Main server loop """
    # Open a socket and loop forever while waiting for clients
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((IP, PORT))
    server_socket.listen()
    print(f"Listening for connections on port {PORT}")

    try:
        while True:
            client_socket, client_address = server_socket.accept()
            print('New connection received')
            handle_client(client_socket)
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        print("Closing server socket.")
        server_socket.close()



def handle_interrupt(signum, frame):
    import sys
    """ Signal handler for SIGINT (Ctrl+C) """
    print(f"Received interrupt signal {signum}. Exiting gracefully.")
    sys.exit(0)  # Exit the program

if __name__ == "__main__":
    # Call the main handler function
    main()
