
import socket
from tkinter import messagebox
from tkinter import *
import sys
import os
import time
HOST = '192.168.1.4' # ip address of server
PORT = 8081
BUFFER = 2048
# Designing window for registration
 
def register(window, client):

    register_screen = Toplevel(window)
    register_screen.title("Register")
    register_screen.geometry("300x250")
    
    
    response = client.recv(BUFFER)
    login_register = 'register'
    client.send(str.encode(login_register))
    if 'quit' in response.decode():
        Label(register_screen, text="Please enter details below", bg="red").pack()
        return
    
    username = StringVar()
    password = StringVar()
 
    Label(register_screen, text="Please enter details below", bg="#9dbeb9").pack()
    Label(register_screen, text="").pack()
    username_lable = Label(register_screen, text="Username * ")
    username_lable.pack()
    username_entry = Entry(register_screen, textvariable=username)
    username_entry.pack()
    password_lable = Label(register_screen, text="Password * ")
    password_lable.pack()
    password_entry = Entry(register_screen, textvariable=password, show='*')
    password_entry.pack()
    Label(register_screen, text="").pack()
    Button(register_screen, text="Register", width=10, height=1, bg="#a3d2ca", 
        command=lambda :register_user(username, password, username_entry, 
                                      password_entry, register_screen, client, window)).pack()
 
 
 
def register_user(username, password, username_entry, password_entry, 
                  register_screen, client, window):
     
    username_info = username.get()
    password_info = password.get()
 
    response = client.recv(BUFFER)
    client.send(str.encode(username_info))
    response = client.recv(BUFFER)
    client.send(str.encode(password_info))
    
    
    username_entry.delete(0, END)
    password_entry.delete(0, END)
    # if Existing username, destroy register_screen
    response = client.recv(BUFFER).decode()
    if 'quit' in response:
        Label(register_screen, text="Existing username",
              fg="red", font=("calibri", 11)).pack()
        window.after(5000, lambda: window.destroy())

    else:
        Label(register_screen, text="Registration Success", 
          fg="#f8a488", font=("calibri", 11)).pack()
        window.after(10000, lambda: window.destroy())

        Button(register_screen, text="Search in library", 
           command=lambda: handle(client)).pack()
 
 
# Designing window for login 
 
def login(window, client):
    login_screen = Toplevel(window)
    login_screen.title("Login")
    login_screen.geometry("300x250")
    Label(login_screen, text="Please enter details below to login").pack()
    Label(login_screen, text="").pack()
    
    response = client.recv(BUFFER)
    login_register = 'login'
    client.send(str.encode(login_register))
    if 'quit' in response.decode():
        Label(login_screen, text="Please enter details below", bg="red").pack()
        return
    
    username_verify = StringVar()
    password_verify = StringVar()
 
    Label(login_screen, text="Username * ").pack()
    username_login_entry = Entry(login_screen, textvariable=username_verify)
    username_login_entry.pack()
    Label(login_screen, text="").pack()
    Label(login_screen, text="Password * ").pack()
    password_login_entry = Entry(login_screen, textvariable=password_verify, show= '*')
    password_login_entry.pack()
    Label(login_screen, text="").pack()
    Button(login_screen, text="Login", width=10, height=1, 
           command=lambda: login_verify(username_verify, password_verify, username_login_entry,
                 password_login_entry, client, login_screen, window)).pack()
 
# Implementing event on register button
 

# Implementing event on login button 
 
def login_verify(username_verify, password_verify, username_login_entry,
                 password_login_entry, client, login_screen, window):
    username_login = username_verify.get()
    password_login = password_verify.get()
    
    response = client.recv(BUFFER)
    client.send(str.encode(username_login))
    response = client.recv(BUFFER)
    client.send(str.encode(password_login))
    
    username_login_entry.delete(0, END)
    password_login_entry.delete(0, END)
 
    response = client.recv(BUFFER).decode()
    if 'Successful' in response:
        login_sucess(login_screen, window, client)
        window.after(7000, lambda: window.destroy())
        

    elif 'Failed' in response:
        password_not_recognised(login_screen)
        window.after(5000, lambda: window.destroy())

        
    else:
        user_not_found(login_screen)
        window.after(5000, lambda: window.destroy())


 
# # Designing popup for login success
def login_sucess(login_screen, window, client):
    login_success_screen = Toplevel(login_screen)
    login_success_screen.title("Success")
    login_success_screen.geometry("150x100")
    Label(login_success_screen, text="Login Success").pack()
    Button(login_success_screen, text="OK", 
           command=lambda: handle(client)).pack()
    
 
# # Designing popup for login invalid password
 
def password_not_recognised(login_screen):
    password_not_recog_screen = Toplevel(login_screen)
    password_not_recog_screen.title("Success")
    password_not_recog_screen.geometry("150x100")
    Label(password_not_recog_screen, text="Invalid Password ").pack()
    Button(password_not_recog_screen, text="OK",
           command=lambda: delete_password_not_recognised(password_not_recog_screen)).pack()
 
# # Designing popup for user not found
 
def user_not_found(login_screen):
    user_not_found_screen = Toplevel(login_screen)
    user_not_found_screen.title("Success")
    user_not_found_screen.geometry("150x100")
    Label(user_not_found_screen, text="User Not Found").pack()
    Button(user_not_found_screen, text="OK", 
           command=lambda: delete_user_not_found_screen(user_not_found_screen)).pack()
 
# # Deleting popups
def delete_login_success(login_success_screen):
    login_success_screen.destroy()
 
 
def delete_password_not_recognised(password_not_recog_screen):
    password_not_recog_screen.destroy()
 
 
def delete_user_not_found_screen(user_not_found_screen):
    user_not_found_screen.destroy()
 
def dowload_book(client, ID_book):
    client.send(str.encode('yes'))
    dowload_book = Tk()
    dowload_book.title("Dowloaded book")
    dowload_book.geometry("500x500")
    response = client.recv(BUFFER)
    response = response.decode()
    Label(dowload_book, text=response, font=("Helvetica", 20), background='#94ebcd').pack()
    if response == 'Good bye':
        Label(read_book, text=response, font=("Helvetica", 20), background='#94ebcd').pack()
        dowload_book.after(5000, lambda:dowload_book.destroy())
    with open(f'{ID_book}.txt', 'w') as file:
       
        Label(dowload_book, text="Receiving data...\nLoading.......", font=("Helvetica", 20), background='#94ebcd').pack()
        data = response
        file.write(data)
        Label(dowload_book, text="Got the file on same folder\nYour file downloaded!!!!", font=("Helvetica", 20), background='#94ebcd').pack()
    
    
 
def read_book(client, handle_window):
    client.send(str.encode('yes'))
    read_book = Tk()
    read_book.title("Read Book")
    read_book.geometry('500x500')
    response = client.recv(BUFFER)
    response = response.decode()
    Label(read_book, text=response, font=("Helvetica", 20), background='#94ebcd').pack()
    if 'quit' in response:
        Label(read_book, text="Disconecting from server",
            font=("Helvetica", 20), background='#94ebcd').pack()
        read_book.after(5000, lambda:read_book.destroy())
    response = client.recv(BUFFER)
    response = response.decode()
    ID_book = response[:11]
    if 'quit' in response:
        Label(read_book, text="Disconecting from server",
            font=("Helvetica", 20), background='#94ebcd').pack()
        read_book.after(5000, lambda:read_book.destroy())
    Button(read_book, text="Dowload book", width=10, height=1, 
           bg="#a3d2ca", command=lambda: dowload_book(client, ID_book)).pack()
 
    
def send_respond(client, request_search, request_search_entry, handle_window):
    request_info1 = request_search_entry.get()
    client.send(str.encode(request_info1))
    request_search_entry.delete(0,END)

    response = client.recv(BUFFER)
    response = response.decode()
    Label(handle_window, text=response, font=("Helvetica", 18), background='#94ebcd').pack()


    if 'quit' in response:
        Label(handle_window, text="Disconecting from server",
            font=("Helvetica", 20), background='#94ebcd').pack()
        handle_window.after(5000, lambda:handle_window.destroy())
        
        
    # request read a book 
    response = client.recv(BUFFER)
    
    if 'quit' in response.decode():
        Label(handle_window, text="Disconecting from server",
            font=("Helvetica", 20), background='#94ebcd').pack()
        handle_window.after(5000, lambda:handle_window.destroy())
    Label(handle_window, text=response.decode()).pack()
    Button(handle_window, text="Read Book", width=10, height=1, 
           bg="#a3d2ca", command=lambda: read_book(client, handle_window)).pack()
# handle with search library
    # search with id
def handle(client):
    handle_window = Tk()
    handle_window.title("Online Library")
    handle_window.geometry('500x700')

 
    Label(handle_window, text="Search in library online", bg="#99bbad", 
          width="300", height="2", font=("Calibri", 13)).pack()
    
    Label(handle_window, text="").pack()
    
    
    
    request_search = StringVar()
    response = client.recv(BUFFER)
    Label(handle_window, text=response.decode()).pack()
    request_search_entry = Entry(handle_window, textvariable=request_search)
    request_search_entry.pack()	
    Label(handle_window, text="").pack()
    Button(handle_window, text="search", width=10, height=1, 
           bg="#a3d2ca", command=lambda: send_respond(client, request_search, request_search_entry, handle_window)).pack()

    handle_window.mainloop()

# Designing Main(first) window

def main_account_screen(client):
    window = Tk()
    window.geometry("500x500")
    window.title("Online Library")
    
    
    Label(text="Select Your Choice", bg="#99bbad", width="300", 
          height="2", font=("Calibri", 13)).pack()
    Label(text="").pack()
    
    Button(text="Login", height="2", width="30", 
           command=lambda: login(window, client)).pack()
    Label(text="").pack()
    Button(text="Register", height="2",
           width="30", command=lambda: register(window, client)).pack()
    
    def on_closing():
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            client.send(str.encode('quit'))
            window.destroy()
    
    window.protocol("WM_DELETE_WINDOW", on_closing)
    window.mainloop()
    
 
 # create an ipv4 (AF_INET) socket object using the tcp protocol (SOCK_STREAM)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connect the client
# client.connect((target, port))
client.connect((HOST, PORT))

main_account_screen(client)