from tkinter import *
from tkinter import ttk
from tkinter import messagebox

import os
import difflib
import serial
import imaplib, re
import time

connected_devices = os.listdir('/dev')
arduino = str(difflib.get_close_matches('tty.usbmodem',connected_devices,1))
arduino = arduino.strip('[]')
arduino = arduino.strip("''")
arduino = '/dev/' + arduino

conn = imaplib.IMAP4_SSL("imap.gmail.com", 993)

previous_unreadcount = 0
unreadCount = 0
do_not_check = 0

def logon():
    global wrong_pass
    global do_not_check
    if do_not_check == 1:
        wrong_pass.grid_forget()
        do_not_check = 0
    try:
        conn.login(user.get(),password.get())
        setup()
        send_username = user.get() + ">"
        ser.write(send_username.encode('utf-8'))
    except:
        do_not_check = 1
        setup()
        exit()
        wrong_pass = ttk.Label(mainframe, text="Incorrect Username or Password", justify = CENTER, foreground = "dark red")
        wrong_pass.grid(column=0, row=3, columnspan = 2)

def setup():
    
    name.grid_remove()
    user_name_entry.grid_remove()
    pasw.grid_remove()
    password_entry.grid_remove()
    login.grid_remove()
    legal.grid_remove()
    password_entry.unbind('<Return>')
    
    global notifier
    notifier = ttk.Label(mainframe, text="Nofifying Gmail for:", justify = CENTER, foreground = "dark red")
    notifier.grid(column=2, row=6, columnspan = 1)
    global working_usr
    working_usr = ttk.Label(mainframe, text = user.get(),foreground = "dark red")
    working_usr.grid(column = 3, row = 6)
    global logout
    logout = ttk.Button(mainframe, text="Log out", command=exit)
    logout.grid(column=2, row=8, columnspan = 2, sticky=(E,W))
    
    if do_not_check != 1:
        check()
        
    
def check():
    global unreadCount
    unreadCount = int(re.search(b"UNSEEN (\d+)", conn.status("INBOX", "(UNSEEN)")[1][0]).group(1))
    if(previous_unreadcount < unreadCount and previous_unreadcount != 0):
        ser.write("One more,".encode('utf-8'))
    if(unreadCount > 0):
        unreadCount_sender =str(unreadCount)
        print(unreadCount_sender)
        ser.write(unreadCount_sender.encode('utf-8'))
        ser.write(",".encode('utf-8'))
    else:
        ser.write("No,".encode('utf-8'))
    recheck()
    
def recheck():
    global previous_unreadcount
    previous_unreadcount = unreadCount
    global re_check
    re_check = root.after(3000,check)

def exit():
    global conn
    conn = imaplib.IMAP4_SSL("imap.gmail.com", 993)
    logout.grid_forget()
    notifier.grid_forget()
    working_usr.grid_forget()
    name.grid()
    global password
    global user
    user = StringVar()
    password = StringVar()
    global user_name_entry
    user_name_entry = ttk.Entry(mainframe, width=20, textvariable=user)
    user_name_entry.grid(column=1, row=0, sticky=(W,E))
    pasw.grid()
    global password_entry
    password_entry = ttk.Entry(mainframe, width=20, show = "*", textvariable=password)
    password_entry.grid()
    password_entry.grid(column=1, row=2, sticky=(W,E))
    login.grid()
    legal.grid()
    user_name_entry.focus()
    password_entry.bind('<Return>', enter)
    if do_not_check != 1:
        root.after_cancel(re_check)
    ser.write("Log out,".encode('utf-8'))
    ser.write("Logged in>".encode('utf-8'))

def enter(event):
    logon()

def not_connected():
    messagebox.showinfo(message='Your Gmail-flag is not connected.  Please connect the flag to your Mac, and restart this the program.')
    root.destroy()


root = Tk()
root.title("Physical Gmail Notifier")


mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))

user = StringVar()
password = StringVar()

name = ttk.Label(mainframe, text="User Name:")
name.grid(column=0, row=0)
user_name_entry = ttk.Entry(mainframe, width=20, textvariable=user)
user_name_entry.grid(column=1, row=0, sticky=(W,E))

pasw = ttk.Label(mainframe, text="Password:")
pasw.grid(column=0, row=2)
password_entry = ttk.Entry(mainframe, width=20, show = "*", textvariable=password)
password_entry.grid(column=1, row=2, sticky=(W,E))

login = ttk.Button(mainframe, text="Login", command=logon)
login.grid(column=0, row=4, columnspan = 2, sticky=(E,W))

legal = ttk.Label(mainframe, text="2012 (c): Philip Gonzalez", justify = CENTER, foreground = "dark red")
legal.grid(column=3, row=6, columnspan = 2) 

frame = ttk.Frame(mainframe, borderwidth=5, relief="sunken", width=200, height=200)
frame.grid(column=2, row=0, columnspan=2, rowspan=6, sticky= N)
label = ttk.Label(frame)
image = PhotoImage(file='gmail.gif')
label['image'] = image
label.grid(column = 0, row = 0)

for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
mainframe.columnconfigure(2, weight=1)
mainframe.rowconfigure(2, weight=1)
root.resizable(FALSE,FALSE)

user_name_entry.focus()
password_entry.bind('<Return>', enter)

try:
    ser = serial.Serial(arduino)
except Exception:
    not_connected()

root.mainloop()
