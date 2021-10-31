'''
Created on Oct 30, 2021

@author: assam
'''
#Assam Ismail
import socket
#Starts up server
def main():
    myServer = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    host = socket.gethostname()

    hostAddress = '0.0.0.0'

    port = 9500

    myServer.bind((hostAddress,port))

    myServer.listen(7)
    return myServer
#Finds error for FileNotFoundError and handles it without closing the server
def ErrorCheck(myServer):

    check = True
    try:
        while check == True:
            myClient,address = myServer.accept()
            print("New incoming connection from",address)
            fileName = myClient.recv(2048)
            directory = myClient.recv(2048)
            print(fileName.decode('utf-8'))
            print(directory.decode('utf-8'))
            clientFile = open(directory,'r')
            process = clientFile.read(1024)
            while process:
                myClient.send(process.encode('utf-8'))
                process = clientFile.read(1024)
            clientFile.close()
            print("Finished procesing")
            myClient.close()
    except ConnectionResetError:
        print("Connection lost with client")
    except FileNotFoundError:
        message1 = ("Sorry, file does not exist")
        print(message1)
        myClient.send(message1.encode('utf-8'))
        ErrorCheck(myServer)
if __name__ == "__main__":
    myServer = main()
    ErrorCheck(myServer)