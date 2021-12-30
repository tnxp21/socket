import socket
import time
import threading
import hashlib
import book

HOST = ''
PORT = 8081
BUFFER = 2048



def read_file_txt(file_name, connection):
    fileText = open(file_name, "r")
    file_not_end = True
    num_of_book = 0
    ID = []
    book_name = []
    author = []
    publish_year = []
    while file_not_end:
        line = fileText.readline().split(',')
        if len(line) == 1:
            file_not_end = False
            break
        
        ID.append(str(line[0]))
        book_name.append(str(line[1]))
        author.append(str(line[2]))
        publish_year.append(str(line[3]))
        
    
    # Request to client search in lirary
    connection.send(str.encode("You can type 'quit' any while to close connection!!!!\nSearch in library: ")) # Request info of book
    book_search = connection.recv(BUFFER).decode()
    current_book_ID = ''
    # 
    if book_search == '':
        connection.send(str.encode('Error with your keyboard(quit)'))
        return
    # search in library with ID
    if 'quit' in book_search:
        connection.send(str.encode('Good bye (quit)'))
        return
    if 'ID' in book_search:
        book_search = str(book_search.split(' ')[1])
        if book_search in ID:
            index_in_library = ID.index(book_search)
            current_book_ID = ID[index_in_library]
            connection.send(str.encode('ID of book : ' + ID[index_in_library] +
                '\nName of book : ' + book_name[index_in_library] +
                '\nPublishing year : ' + publish_year[index_in_library] +
                'Auther of book : '+ author[index_in_library]))
        else:
            connection.send(str.encode('Your ID not in library !!!(quit)' ))
            return
            
        
    # search in library with Name
    elif 'Name' in book_search:
        book_search = book_search[8:(len(book_search) - 1)]
        if book_search in book_name:
            index_in_library = book_name.index(book_search)
            current_book_ID = ID[index_in_library]
            connection.send(str.encode('ID of book : ' + ID[index_in_library] +
                '\nName of book : ' + book_name[index_in_library] +
                '\nPublishing year : ' + publish_year[index_in_library] +
                'Auther of book : '+ author[index_in_library]))
        else:
            connection.send(str.encode('Your Book not in library !!!(quit)'))
            return
            

    elif 'Type' in book_search:
        book_search = book_search[8:(len(book_search) - 1)]
        if book_search in book.type_of_books:
            same_type = [v for k,v in book.type_of_books.items() if k == book_search][0]
            mess = ''
            for i in range(0, len(same_type)):
                index_in_library = ID.index(same_type[i])
                current_book_ID = ID[index_in_library]
                mess = '\n'.join([mess, 'ID of book : ' + ID[index_in_library] +
                '\nName of book : ' + book_name[index_in_library] +
                '\nPublishing year : ' + publish_year[index_in_library] +
                'Auther of book : '+ author[index_in_library]])
            connection.send(str.encode(mess))
            time.sleep(1)  
        else:
            connection.send(str.encode('Your Book not in library !!!(quit)'))
            return
    elif 'Author' in book_search:
        book_search = book_search[10:(len(book_search) - 1)]
        if book_search in book.author_of_books:
            same_type = [v for k,v in book.author_of_books.items() if k == book_search][0]
            mess = ''
            for i in range(0, len(same_type)):
                index_in_library = ID.index(same_type[i])
                current_book_ID = ID[index_in_library]
                mess = '\n'.join([mess, 'ID of book : ' + ID[index_in_library] +
                '\nName of book : ' + book_name[index_in_library] +
                '\nPublishing year : ' + publish_year[index_in_library] +
                'Auther of book : '+ author[index_in_library]])
            connection.send(str.encode(mess))
            time.sleep(1)  
        else:
            connection.send(str.encode('Your Book not in library !!!(quit)'))
            return
            
    else:
        connection.send(str.encode('Your searching not in library!!!(quit)'))
        return
    time.sleep(1)  

    
    # read book
    connection.send(str.encode('You want to read this book(yes/no): ')) 
    is_read_book = connection.recv(BUFFER).decode()
    if is_read_book == '':
        connection.send(str.encode('Your searching not in library!!! Good bye(quit)'))
        return
    if 'quit' in is_read_book:
        connection.send(str.encode('Good bye (quit)'))
        return
        
    if is_read_book == 'yes':
        connection.send(str.encode(book.ID_ReadBook[current_book_ID]))
    elif is_read_book != 'yes':
        connection.send(str.encode('Good bye'))
    
    time.sleep(1)  
    # dowload book
    connection.send(str.encode(f'Book_ID_{ID[index_in_library]} You want to download this book(yes/no): ')) 
    download_book = connection.recv(BUFFER).decode()
    if download_book == '':
        connection.send(str.encode('Keyboard error!!!(quit)'))
        return
    if 'quit' in download_book:
        connection.send(str.encode('Good bye (quit)'))
    elif download_book == 'yes':
        path_to_dowload_book = f'book_file/{ID[index_in_library]}.txt'
        with open(path_to_dowload_book, 'rb') as file:
            data = file.read(BUFFER)
            while data:
                connection.send(data)
                data = file.read(BUFFER)
    elif download_book != 'yes':
        connection.send(str.encode('Good bye'))
        


# Create Socket (TCP) Connection

HashTable = {}
# function input username and password
def input_username_password(connection, name, password):
    name, password = '', ''
    connection.send(str.encode('ENTER USERNAME : ')) # Request Username
    name = connection.recv(BUFFER)
    name = name.decode()
    if name == '':
        print('Disconnected from client')
        connection.close()
        return name, password
    connection.send(str.encode('ENTER PASSWORD : ')) # Request Password
    password = connection.recv(BUFFER)
    password = password.decode()
    if password == '':
        print('Disconnected from client')
        connection.close()
        return name, password
    password=hashlib.sha256(str.encode(password)).hexdigest() # Password hash using SHA256
    return name, password



# Function : For each client 
def threaded_client(connection):
    connection.send(str.encode('Type login or register!!!: '))
    login_register = connection.recv(BUFFER).decode()
    hash = {}
    password_list = []
    username_list = []
    name = ''
    password = ''
    with open("info_user.txt") as fileread:
        for line in fileread:
            name_login, password_login = line.strip().split('.', 1)
            hash[name_login] = password_login
            password_list.append(password_login)
            username_list.append(name_login)
            
    if 'login' in login_register:
        
        name, password = input_username_password(connection, name, password)
        if name == '' or password == '':
            return
        
        
        # if correct
        if name in username_list:
            if password in password_list:
                connection.send(str.encode('Connection Successful')) # Response Code for Connected Client 
                print('Connected : ',name)
            else:
                connection.send(str.encode('Login Failed\nDisconnected from server(quit)')) # Response code for login failed
                print('Connection denied : ',name)
                connection.close()
                return
        
        else:
            connection.send(str.encode(' User not found\nDisconnected from server(quit)')) # Response code for login failed
            print('Connection denied : ',name)
            connection.close()
            return
            
        
    elif 'register' in login_register:
        name, password = input_username_password(connection, name, password)
        if name in hash:
            connection.send(str.encode('Existing username!!\nDisconnected from server(quit)')) # Response code for login failed
            print('Connection denied : ',name)
            connection.close()
            return 
        with open("info_user.txt", "a") as f:
            f.write(name + '.' + password + '\n')
        hash[name]=password
        connection.send(str.encode('Registeration Successful')) 
        print('Registered : ',name)
        print("{:<8} {:<20}".format('USER','PASSWORD'))
        for k, v in HashTable.items():
            label, num = k,v
            print("{:<8} {:<20}".format(label, num))
        print("-------------------------------------------")
    else:
            connection.send(str.encode('Wrong syntax\nDisconnected from server(quit)')) # Response code for login failed
            print('Connection denied : ',name)
            connection.close()
            return
    
    while True:
        read_file_txt("library.txt", connection)
        print("Connection close")
        connection.close()
        return



ServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

ThreadCount = 0
try:
    ServerSocket.bind((HOST, PORT))
except socket.error as e:
    print(str(e))

print('Waitiing for a Connection..')
ServerSocket.listen(5)

while True:
    Client, address = ServerSocket.accept()
    client_handler = threading.Thread(
        target=threaded_client,
        args=(Client, ))
    client_handler.start()
    ThreadCount += 1
    print('Connection Request: ' + str(ThreadCount))  
    print(f"[NEW CONNECTION] {address} connected.")
        
ServerSocket.close()