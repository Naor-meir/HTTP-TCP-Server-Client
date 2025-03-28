import socket
import sys

def send_message(client, path_file):
     message = ( f"GET {path_file} HTTP/1.1\r\nConnection: close\r\n\r\n")
     client.sendall(message.encode())
     response = client.recv(1024).decode()
     return response

def ok_response(header_lines,data,client,name_file):
        
        #set the file size to 0
        file_size = 0
        #get the line that contain the file size
        for line in header_lines:
            if line.startswith("Content-Length"):
                # Split by space and get the last part (file size)
                file_size = int(line.split(" ")[1].strip())
                break
        # Check if the file size is greater than 0 and the data is not empty 
        while (len(data) < file_size):
            # Receive the rest of the
            data += client.recv(1024)
            file_name = name_file.strip().split("/")[-1] or "index.html"
            # file_name="files/"  + file_name
            # Save the file in the client's directory
            with open(file_name, "wb") as f:
                f.write(data)  # Write the content received from the serve
def move301_response(header_lines): 
    path_file = None
    for line in header_lines:
         if line.startswith("Location:"):
             path_file=line.split(" ")[1]
             break
    return path_file
             


if __name__ == "__main__":
    ip = sys.argv[1]  # Get the IP address from the first argument
    port = int(sys.argv[2])  # Get the PORT address from the second argument
    redirect_flag = False
    # client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    while True:
        #check if the user want to redirect
        if not redirect_flag :
            ##get the path from the user
            path_file=input()
            #send the message to the server and recive the response
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((ip, port))
        response=send_message(client,path_file)
        #split the response to header and data
        header, data = response.split("\r\n\r\n", 1)
        # Convert the string back to bytes
        data = data.encode('utf-8')  
        # Split the header into lines
        header_lines = header.split("\r\n")   
        # Print the first line of the header
        print(header_lines[0])
        # Check if the response is OK
        if header_lines[0].endswith("OK"):
        # Call the function to handle the OK response
          ok_response(header_lines,data,client,path_file)
          # Set the redirect flag to False
          redirect_flag = False
          # Check if the response is a 301 Moved Permanently
        elif header_lines[0].endswith("Moved Permanently"):
            # Call the function to handle the 301 response and get the new path from the response header  in the location field
            path_file = move301_response(header_lines)
            # Set the redirect flag to True
            redirect_flag = True
            # Check if the response is a 404 Not Found
        else: redirect_flag = False
        
   
    
