# HTTP_server_shell.py
# This file contains the main server logic for the HTTP server implementation.
import os
import socket
import HTTP_protocol as protocol

# Constants for the server
IP = '0.0.0.0'
PORT = 80
SOCKET_TIMEOUT = 0.5

# Constants for the HTTP server
RESOURCE_FOLDER = 'webroot'
REDIRECTION_DICTIONARY = {
    '/doremon': 'css/doremon.css',
    '/abstract': 'imgs/abstract.jpg',
    '/favicon': 'imgs/favicon.ico',
    '/loading': 'imgs/loading.gif',
    '/index': 'index.html',
    '/box': 'js/box.js',
    '/jquery': 'jquery.min.js',
    '/submit': 'js/submit.js',

    '/': 'index.html' # Default url
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
    

def serve_client_request(resource, client_socket):
    """ Serve client requests based on the resource """
    try:
        if resource in REDIRECTION_DICTIONARY:
            new_location = REDIRECTION_DICTIONARY[resource]
            print(f"Redirecting {resource} to {new_location}")
            client_socket.send(protocol.generate_status_code(302, location=new_location))
        else:
            # Convert '/' to '\\' in the resource path
            normalized_resource = resource.replace('/', '\\')
            requested_file = os.path.join(RESOURCE_FOLDER, normalized_resource.lstrip('\\'))
            data = get_file_data(requested_file)
            if data is not None:
                filetype = resource.split('.')[-1] if '.' in resource else 'html'
                client_socket.send(protocol.generate_status_code(200, protocol.get_content_type(filetype), data))
            else:
                client_socket.send(protocol.generate_status_code(404))
    except Exception as e:
        print(f"Exception occurred while handling request: {e}")
        client_socket.send(protocol.generate_status_code(500))


def handle_client(client_socket):
    """ Handle client connections """
    try:
        client_socket.settimeout(SOCKET_TIMEOUT)
        request_data = client_socket.recv(1024).decode()
        valid_request, resource = protocol.validate_http_request(request_data)
        if valid_request:
            serve_client_request(resource, client_socket)
        else:
            client_socket.send(protocol.generate_status_code(404))
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
    print("Listening for connections on port {}".format(PORT))

    # Register signal handler for SIGINT (Ctrl+C)
    signal.signal(signal.SIGINT, handle_interrupt)

    try:
        while True:
            client_socket, client_address = server_socket.accept()
            print('New connection received')
            handle_client(client_socket)
    except Exception as e:
        print(f"Error occurred: {e}")
        handle_interrupt(signal.SIGINT, None, server_socket)  # Handle interrupt on error
    finally:
        print("Server interrupted. Closing server socket.")
        server_socket.close()
        print("Server socket closed. Goodbye!")


def handle_interrupt(signum, frame, server_socket):
    import sys
    """ Signal handler for SIGINT (Ctrl+C) """
    print(f"Received interrupt signal {signum}. Exiting gracefully.")
    server_socket.close()  # Close server socket
    sys.exit(0)  # Exit the program


if __name__ == "__main__":
    # Call the main handler function
    main()