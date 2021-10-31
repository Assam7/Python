'''
Created on Jan 13, 2021

@author: assam
'''
from sys import argv
def ListofTokens(path):#O(n) function will run through n number of lines linear time
    value1 = []
    file_name = open(path, 'r', 1, 'utf-8')
    for x in file_name:
        line = x.rstrip('\n')
        value = line.split()
        for y in value:
            if y.isalnum() == False:
                string1 = ''
                for char in y:
                    if char.isalnum() == True:
                        string1+=char
                    else:
                        if len(string1) >0:
                            value.append(string1)
                        string1 = ''
                if len(string1)>0:
                    value.append(string1)
                value.remove(y)
        value1 += value
    return value1
def constructDiction(value):#linear time O(n) because i go through each value in the list of tokens only once
    diction = {}
    for y in value:
        if y.lower() not in diction.keys():
            diction[y.lower()] = 1
        else:
            diction[y.lower()] +=1 
    return diction
def printAll(diction):#O(n) because i go through the sorted dictionary only one time linear time
    item = sorted(diction.items(), key=lambda x: (-x[1],x[0]), reverse=False)
    for k,v in item:
        print(k+'\t'+str(v)) 
if __name__ == '__main__': 
    file_name = argv[1]
    value = ListofTokens(file_name)
    diction = constructDiction(value)
    printAll(diction)