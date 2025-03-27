# HTTP Server Project

## Summary
This project implements a custom HTTP server and client in Python. The server listens on a specified port, serves static files, and returns appropriate status codes (200, 404, 301). The client demonstrates persistent connections (keep-alive) and automatically reconnects if the connection is unexpectedly lost.

## Key Features

### Server
- **Purpose**: Listens for incoming HTTP requests and serves files from a designated directory.  
- **Functionality**:  
  - Listens on a specified TCP port.  
  - Serves static files (e.g., HTML, images) from a dedicated folder.  
  - Handles HTTP GET requests.  
  - Responds with status codes such as 200 (OK), 404 (Not Found), and 301 (Moved Permanently).  
  - Logs request and response headers.

### Client
- **Purpose**: Sends HTTP GET requests to the server and supports connection persistence.  
- **Functionality**:  
  - Sends HTTP GET requests to a specified server IP and port.  
  - Supports `Connection: keep-alive` for maintaining a continuous connection.  
  - Automatically reconnects and resends the last request if the connection is unexpectedly lost.

## What I Learned
- Managing TCP sockets and structuring request-response flows in Python.  
- Handling file operations and status codes in a web-related environment.  
- Implementing and testing persistent connections and reconnection logic.  
- Organizing server-client projects that involve logging and clear error reporting.

## How to Run

### Server
The server starts listening for incoming requests on the specified port.
```bash
python3 server.py <port>
'''
Example:
```bash
python3 server.py 8080
'''
### Client 
After connecting, enter the file path you wish to request. The client will handle unexpected disconnections by attempting to reconnect and resend the previous request.
''' bash
python3 client.py <server-ip> <server-port>
'''
Example :
''' bash
python3 client.py 127.0.0.1 8080

Client
After connecting, enter the file path you wish to request.
The client will handle unexpected disconnections by attempting to reconnect and resend the last request.

bash
Copy
Edit
python3 client.py <server-ip> <server-port>
Example:

bash
Copy
Edit
python3 client.py 127.0.0.1 8080
javascript
Copy
Edit



