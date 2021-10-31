'''
Created on Oct 30, 2021

@author: assam
'''
#Assam Ismail
import socket
import CheckFile
#Runs Client side of program
def main():
    myClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client = socket.gethostname()
    clientIP = socket.gethostbyname(client)
    print(clientIP)
    port = 9500
    serverAddr = '127.0.0.1'
    myClient.connect((serverAddr,port))
    comparison = ''
    path,txtPath,directory = CheckFile.CheckDir() #Checks if directory is valid and creates a directory for the ClientReports
    myClient.send(directory.encode('utf-8'))
    myClient.send(txtPath.encode('utf-8'))
    reportsDir = CheckFile.ReportsPath(path,txtPath)
    check = True
    if check == True:
        error = myClient.recv(1024)
        error1 = error.decode('utf-8')
        if error1 == "Sorry, file does not exist":
            print(error1)
            main()
    incomingData = myClient.recv(1024)
    newClient = open(reportsDir/"Lab4.txt", 'w')
    newClient.write(error1)
    while incomingData:
        new = incomingData.decode('utf-8')
        newClient.write(new)
        incomingData = myClient.recv(1024)
    newClient.close()
    myClient.close()
if __name__ == "__main__":
    main()