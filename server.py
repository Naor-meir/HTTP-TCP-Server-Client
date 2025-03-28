import socket 
import sys
import os

# Define ROOT_DIR as the absolute path to your local directory
ROOT_DIR = "files"


def create_server(port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("", port))  # Bind to all available network interfaces
    server.listen(5)  # Max number of queued connections
    return server 

def send_redirect_response(client_socket):
    response = (
        "HTTP/1.1 301 Moved Permanently\r\n"
        "Connection: close\r\n"
        "Location: /result.html\r\n"
        "\r\n"  # Blank line to separate headers from the body
    )
    client_socket.sendall(response.encode('utf-8'))
    client_socket.close()

def send_notFound_response(client_socket):
    response = "HTTP/1.1 404 Not Found\r\nConnection: close\r\n\r\n"
    client_socket.sendall(response.encode('utf-8'))
    client_socket.close()

def send_image_response(client_socket, target_file, connection):
    with open(target_file, 'rb') as file:
        binary_data = file.read()
        length = len(binary_data)
    response_headers = (
            "HTTP/1.1 200 OK\r\n"
            f"Connection: {connection}\r\n"
            f"Content-Length: {length}\r\n"
            "\r\n"
        )
    client_socket.sendall(response_headers.encode('utf-8'))
    client_socket.sendall(binary_data)
    if connection == 'close':
         client_socket.close()

def send_file_response(client_socket, target_file, connection):
    with open(target_file, 'r') as file:
        file_body = file.read()
        content_length = len(file_body)
    response_headers = (
        f"HTTP/1.1 200 OK\r\n"
        f"Connection: {connection}\r\n"
        f"Content-Length: {content_length}\r\n"
        "\r\n"
    )
    client_socket.sendall(response_headers.encode('utf-8'))
    client_socket.sendall(file_body.encode('utf-8'))  # Encoding the body as UTF-8
    
    if connection == 'close':
        client_socket.close()

def receive_until_two_empty_lines(client_socket):
    data = ""
    try:
        while True:
            chunk = client_socket.recv(1024).decode('utf-8')
            if not chunk:
                return None 
            else:
                data += chunk
                if "\r\n\r\n" in data:  # End of HTTP headers
                    print(data)
                    return data  # Return the data after receiving the full headers
    except socket.timeout:
        return None



def handle_request(request, connection, client_socket):
     path = request.split(" ")[1]
     if"//" in path:
        send_notFound_response(client_socket)
     else:    
        path = path.lstrip("/") 
        directory, filename = os.path.split(path) 
        if not filename:
            filename = "index.html"  # Default filename
        target_file = os.path.join(ROOT_DIR, directory, filename)  # Construct the full path
        

        if filename == "redirect":  # Handle redirect
            send_redirect_response(client_socket)
        elif not os.path.isfile(target_file):  # If file doesn't exist, send a 404
            send_notFound_response(client_socket)
        elif target_file.endswith(('.jpg', '.ico')):  # Send binary image data
            send_image_response(client_socket, target_file, connection)
        else:  # For other types of files
            send_file_response(client_socket, target_file, connection)

if __name__ == "__main__":
    portA = int(sys.argv[1])
    server = create_server(portA)
    while True:
        client_socket, client_address = server.accept()
        client_socket.settimeout(1)
        client_message = receive_until_two_empty_lines(client_socket)
        if client_message is None:
            client_socket.close()
        else:
            lines = client_message.split("\r\n")
            request_line = lines[0]
            connection_value = None
            for line in lines:
                if line.startswith("Connection:"):
                    connection_value = line.split(":")[1].strip()  # Extract the connection value
                    break
            handle_request(request_line, connection_value, client_socket)
