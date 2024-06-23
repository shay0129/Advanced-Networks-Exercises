# HTTP_protocol.py
# This file contains constants and functions related to the HTTP protocol for the HTTP server implementation.

VALID_METHODS = {'GET'}  # add POST, PUT, DELETE, etc. if needed

STATUS_MESSAGES = {
    200: 'OK',
    302: 'Found',
    404: 'Not Found',
    500: 'Internal Server Error',
    403: 'Forbidden'
}

DEFAULT_BODIES = {
    200: b"200 OK\r\nThe request was successful.",
    302: lambda loc: f"302 Found\r\nThe document has moved '{loc}' here.".encode(),
    404: b"404 Not Found\r\nThe requested resource could not be found.",
    500: b"500 Internal Server Error\r\nThere was an error processing your request.",
    403: b"403 Forbidden\r\nYou do not have permission to access this resource."
}

def generate_response_header(status_code, content_type='text/html', location=None):
    """ Generate the HTTP response header with the given status code and content type """
    status_message = STATUS_MESSAGES.get(status_code, 'Unknown Status')  # Default to 'Unknown Status' if status code is not found
    response_header = f"HTTP/1.1 {status_code} {status_message}\r\nContent-Type: {content_type}\r\n"

    if location and status_code == 302:
        response_header += f"Location: {location}\r\n"
    
    return response_header

def generate_response_body(status_code, location=None):
    """ Generate the HTTP response body based on the given status code """
    try:
        if status_code == 302 and location:
            return DEFAULT_BODIES[302](location)
        else:
            return DEFAULT_BODIES.get(status_code, b"")
    except KeyError:
        return b""

def generate_status_code(status_code, content_type='text/html', response_body=None, location=None):
    """ Generate the complete HTTP response with header and body """
    response_header = generate_response_header(status_code, content_type, location)
    if response_body is None:
        response_body = generate_response_body(status_code, location)

    response_header += f"Content-Length: {len(response_body)}\r\n\r\n"

    return response_header.encode() + response_body  # Return the response header and body as bytes

def get_content_type(filetype):
    """ Determine content type based on file extension
        sample: filetype = 'css', return 'text/css'"""
    content_types = {
        'html': 'text/html; charset=utf-8',
        'css': 'text/css',
        'jpg': 'image/jpeg',
        'jpeg': 'image/jpeg',
        'png': 'image/png',
        'gif': 'image/gif',
        'js': 'application/javascript',
    }
    return content_types.get(filetype, 'text/plain')  # Default to plain text if type is unknown

def validate_http_request(request):
    """ Validate the incoming HTTP request.
        sample: request = 'GET /index.html HTTP/1.1', return True, '/index.html' """
    parts = request.split(' ')
    if len(parts) >= 2 and parts[0] in VALID_METHODS:
        return True, parts[1]
    return False, None
