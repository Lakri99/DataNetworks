# 
# Import socket library and Hash(MD5) library
#
from socket import *
import hashlib
import glob
import os
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
# 
# Create TCP socket for future connections

serverSocket = socket(AF_INET, SOCK_STREAM)
# serverSocket.TCPServer.allow_reuse_address = True
# 
# Bind URL and Port to the created socket
#
serverSocket.bind((serverURL, serverPort))
# 
# Start listening for incoming connection (1 client at a time)
#
serverSocket.listen(1)
print("Server is listening on port: " + str(serverPort))
file_dict = {'6008994857f03e089549f58db518f5d9': 'The_file.jpg'}

def list(connectSocket):
    mylist = [f for f in glob.glob("*.jpg")]
    if not mylist:
        message = "There are no files available"
    else:
        message = ""
        for filename in  mylist:
            md5 = generate_md5_hash(open(filename, "rb").read())
            message = message + str(md5) + ";" + str(filename) + ';' + str(os.path.getsize(filename))
            print(filename)
    connectSocket.sendall(bytes(message, 'ascii'))
    return

def upload(connectSocket):
    message = "Please send the file name and file size"
    connectSocket.send(bytes(message, 'ascii')) 
    result = connectSocket.recv(4096)
    result = result.decode("UTF-8").split(";")
    print(result)
    if len(result) > 1:
        message = "READY"
        connectSocket.send(bytes(message, 'ascii')) 
        filename = result[0]
        filesize = int(result[1])
        data = b''
        data += connectSocket.recv(filesize)
        print(len(data))
        data += connectSocket.recv(filesize)
        data += connectSocket.recv(filesize)
        f = open(filename, 'wb')
        f.write(data)
        hash = generate_md5_hash(data)
        file_dict[hash] = filename
        print(hash)
        connectSocket.send(bytes(hash, 'utf-8'))
        result = connectSocket.recv(filesize)
        print("Message from client: " + result.decode('utf-8'))  
    else:
        message = "Incorrect details"
        connectSocket.send(bytes(message, 'ascii'))

def download(connectSocket):
    message = "SEND fileid"
    connectSocket.sendall(bytes(message, 'ascii')) 
    result = connectSocket.recv(4096)
    result = result.decode('utf-8')
    filename = file_dict.get(result, 'None')
    print("saved dictionary")
    print(file_dict)
    if filename:
        data = open(filename, 'rb')
        data = data.read()
        connectSocket.send(data)

    else:
        message = "File not avaialabel"
        connectSocket.send(bytes(message, 'ascii'))
        result = connectSocket.recv(4096)
        result = result.decode('utf-8')
    return

while True:
    # 
    # Accept incoming client connection
    #
    connectSocket, addr = serverSocket.accept()
    print("Client connected: " + str(addr))

    command = connectSocket.recv(4096)
    command = command.decode("UTF-8")
    print(" Message recieved from client: " + command)
    #close TCP connection

    if command == 'LIST_FILES':

        list(serverSocket)

    if command == 'UPLOAD':
        upload(connectSocket)
            
    
    if command == 'DOWNLOAD':
        download(connectSocket)


        



    connectSocket.close()