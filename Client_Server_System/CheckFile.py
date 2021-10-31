'''
Created on Oct 30, 2021

@author: assam
'''
#Assam Ismail
from pathlib import Path
#Ensures directory and fileDir are valid. Checks to make sure directory is not a file
#Makes sure fileDir is a txt file
def CheckDir():
    directory = input("Enter the directory of the file you wish to transfer: ")
    p = Path(directory)
    while p.is_file() ==  True:
        print("Enter directory without the file included!")
        directory = input("Enter the directory of the file you wish to transfer: ")
    fileDir = input("Now just input the text file name: ")
    comparison = fileDir[-4:]
    while comparison != '.txt':
        comparison = fileDir[-4:]
    p = Path(directory)
    print(type(p))
    validation = p.exists()
    print(validation)
    while validation == False:
        print("Directory does not exist! Please enter a valid directory for the txt file.")
        CheckDir()
    print(p)
    return p,fileDir,directory
#Creates the ClientReports folder
def ReportsPath(p,fileDir):
    confirmation = input("Do you want to add the text file to a ClientReports Folder in the same directory.\nEnter y for yes to create the folder: ")
    while confirmation.upper() != 'Y':
        print("Try Again!")
        confirmation = input("Do you want to add the consolidated file and text file to a Reports Folder in the same directory.\nEnter y for yes to create the folder: ")
    rDir = p.joinpath("ClientReports")
    print(rDir)
    Path(rDir).mkdir(parents=True, exist_ok=True)
    print(rDir.exists())
    return rDir