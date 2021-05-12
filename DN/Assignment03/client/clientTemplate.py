# 
# Import socket library and Hash(MD5) library
#
from socket import *
import hashlib
import os
import sys
#
# Generate md5 hash function
#
def generate_md5_hash (file_data):
    md5_hash = hashlib.md5(file_data)
    f_id = md5_hash.hexdigest()
    return str(f_id)
# 
# Define Server URL and PORT
#
serverPort = 7701
serverURL = "localhost"
FORMAT = "UTF-8"

# 
# Get the command from cmd line arg
# 
command = sys.argv[1]

# 
# Create TCP socket for future connections
#
clientSocket = socket(AF_INET, SOCK_STREAM)
# clientSocket.TCPServer.allow_reuse_address = True
# 
# Connect the client to the specified server
#
clientSocket.connect((serverURL, serverPort))
print("Client connected to server: " + serverURL + ":" + str(serverPort))
#
# This client implements the following scenario:
# 1. LIST_FILES
# 2a. UPLOAD the specified file
# 2b. Check MD5
# 3. LIST_FILES
# 4a. DOWNLOAD the previously uploaded file
# 4b. Check MD5
#
#close TCP connection

# Send list files 
def list(clientSocket):
    clientSocket.send(b'LIST_FILES')
    result = clientSocket.recv(4096)
    result = result.decode("UTF-8")
    print("\n Result from server: " + result)

# Upload files
def upload(clientSocket):
    clientSocket.send(b'UPLOAD')
    result = clientSocket.recv(4096)
    result = result.decode("UTF-8")
    print("\n Message from server: ", result)
    if result:
        filename = 'The_file.jpg'
        filesize = os.path.getsize(filename)
        message = bytes(filename + ';'+str(filesize), FORMAT)
        clientSocket.send(message)
        result = clientSocket.recv(4096)
        result = result.decode(FORMAT)
        if result == 'READY':
            data = open(filename, 'rb')
            data = data.read()
            clientSocket.sendall(data)
            hash_rec = clientSocket.recv(4096)
            hash_gen = generate_md5_hash(data)
            if hash_rec.decode('utf-8') == hash_gen:
                clientSocket.send(b'SUCCESS')

# DOWNLOAD
def download(clientSocket, fileid_rec):
    # fileid_rec = '6008994857f03e089549f58db518f5d9'
    clientSocket.send(b'DOWNLOAD')
    result = clientSocket.recv(1024)
    result = result.decode("UTF-8")
    print("\n Message from server: " + result)
    clientSocket.send(bytes(fileid_rec, 'utf-8'))

    data = b''
    data += clientSocket.recv(65536)
    data += clientSocket.recv(65536)
    data += clientSocket.recv(65536)
    hash = generate_md5_hash(data)
    if hash == fileid_rec:
        clientSocket.send(b'SUCCESS')


if command == "LIST":
    list(clientSocket)
elif command == "UPLOAD":
    upload(clientSocket)
elif command == "DOWNLOAD":
    fileid_rec = sys.argv[2]
    if fileid_rec:
        download(clientSocket, fileid_rec)
    else:
        print("\n Incorrect file ID, please try again...")

clientSocket.close()
