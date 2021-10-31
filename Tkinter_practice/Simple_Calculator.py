'''
Created on Oct 30, 2021

@author: assam
'''
#Assam Ismail
import tkinter as tk
class CustomException(Exception):
    pass
def InvalidInput(seconds):
    try:
        if seconds.isdigit() == False:
            text = ("Invalid Input")
            return text
    except AttributeError:
        if int(seconds) < 0:
            text = ("Invalid Input")
            return text
def minutesConv(seconds):
    temp = (str(seconds // 60)+" minute(s)")
    return temp
def hoursConv(seconds):
    temp = (str(seconds // 3600)+" hour(s)")
    return temp
def daysConv(seconds):
    temp = (str(seconds // 86400)+" day(s)")
    return temp
def converter(entry,Option,value):
    seconds = entry.get()
    try:
        if seconds.isdigit() == True:
            if int(seconds) >= 0:
                seconds = int(entry.get())
            OptionVal = Option.get()
            if OptionVal == "Seconds to minutes":
                temp = minutesConv(seconds)
                value.set(temp)
            elif OptionVal == "Seconds to hours":
                temp = hoursConv(seconds)
                value.set(temp)
            else:
                temp = daysConv(seconds)
                value.set(temp)
        else:
            raise CustomException
    except CustomException:
        text = InvalidInput(seconds)
        entry.delete(0,len(seconds))
        entry.insert(0,text)
        entry.grid(row=8,column=5)
        value.set(0)
        print("Error found")
def main():
    root = tk.Tk()
    root.title("Seconds Converter")
    root.geometry('400x400')
    Option = tk.StringVar()
    prompt = tk.StringVar().set("Enter the number of seconds you want to convert: ")
    value = tk.IntVar()
    prompt1 = tk.Label(master=root,text="Welcome to Seconds Converter!")
    prompt1.grid(row=0,column=0)
    prompt2 = tk.Label(master=root,text="Convert to:").grid(row=4,sticky="W")
    Option.set("Seconds to minutes")
    option = tk.OptionMenu(root, Option,"Seconds to minutes","Seconds to hours", "Seconds to days")
    option.grid(row=4,column= 5)
    layout = tk.Label(master=root,text="Seconds to Convert:")
    layout.grid(row=8,sticky="W")
    entry = tk.Entry(master=root,textvariable=prompt,fg="blue")
    entry.grid(row=8,column=5)
    answerL = tk.Label(master=root,text="Result")
    answerL.grid(row=10,sticky="W")
    conVal = tk.Label(master=root,fg="blue",bg="White",textvariable=value).grid(row=10,column=5)
    button = tk.Button(master=root, bg="blue", text="Convert",command=lambda: converter(entry,Option,value))
    button.grid(row=14,column=5)
    qbutton = tk.Button(master=root, bg="red", text="Quit",command=root.destroy)
    qbutton.grid(row=14,column=3)
    root.mainloop()
if __name__ == '__main__':
    main()

