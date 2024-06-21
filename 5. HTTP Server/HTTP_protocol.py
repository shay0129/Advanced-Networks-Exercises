# HTTP_protocol.py
# This file contains constants and functions related to the HTTP protocol for the HTTP server implementation.

status_messages = {
        200: 'OK',
        302: 'Found',
        404: 'Not Found',
        500: 'Internal Server Error',
        403: 'Forbidden'
    }

default_bodies = {
        200: b"<html><body><h1>200 OK</h1><p>The request was successful.</p></body></html>",
        302: lambda loc: f"<html><body><h1>302 Found</h1><p>The document has moved <a href='{loc}'>here</a>.</p></body></html>".encode(),
        404: b"<html><body><h1>404 Not Found</h1><p>The requested resource could not be found.</p></body></html>",
        500: b"<html><body><h1>500 Internal Server Error</h1><p>There was an error processing your request.</p></body></html>",
        403: b"<html><body><h1>403 Forbidden</h1><p>You do not have permission to access this resource.</p></body></html>"
    }

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
    return content_types.get(filetype, 'text/plain') # Default to plain text if type is unknown


def generate_status_code(status_code, content_type='text/html', response_body=None, location=None):
    """ Generate an HTTP response with the given status code.
        sample: status_code = 200, return response_header (OK) + response_body (200 OK The request was successful)"""
    status_message = status_messages.get(status_code, 'Unknown Status') # Default to 'Unknown Status' if status code is not found
    response_header = f"HTTP/1.1 {status_code} {status_message}\r\nContent-Type: {content_type}\r\n"
    
    if location and status_code == 302:
        response_header += f"Location: {location}\r\n"
        response_body = default_bodies[302](location)
    
    if response_body is None:
        response_body = default_bodies.get(status_code, b"") # Default to an empty body if status code is not found
    
    response_header += f"Content-Length: {len(response_body)}\r\n\r\n"
    
    return response_header.encode() + response_body # Return the response header and body as bytes


def validate_http_request(request):
    """ Validate the incoming HTTP request.
        sample: request = 'GET /index.html HTTP/1.1', return True, '/index.html'"""
    parts = request.split(' ')
    if len(parts) >= 2 and (parts[0] == 'GET' or parts[0] == 'HEAD' or parts[0] == 'POST' or parts[0] == 'PUT' or parts[0] == 'DELETE'):
        return True, parts[1]
    return False, None