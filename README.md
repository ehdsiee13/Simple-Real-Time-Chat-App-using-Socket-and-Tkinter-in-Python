# Simple-Real-Time-Chat-App-using-Socket-and-Tkinter-in-Python

# In this activity, we will create a simple real-time chat application using Socket and Tkinter in Python programming language. The application will allow users to communicate with each other in real-time using a graphical user interface built with Tkinter. Socket programming will enable the exchange of messages between users over the internet. The goal of this project is to create a working chat application that can be used as a foundation for more complex applications.


# The first thing is to create a server and then import the necessary modules for creating a server with socket communication and managing threads.

    import socket
    import threading


# Next is to define the host IP address, port number, and the maximum number or queued connections for the server socket.
# The host is the standard loopback interface address (localhost)
# The port is to listen on (non-privileged ports are > 1023)
# The listener limit is to limit the connections for the server socket

    HOST = '192.168.1.127'
    PORT = 1234
    LISTENER_LIMIT = 5


# Then add list to keep track of connected clients. Each element in the list is a tuple containing the username and the client socket.

    active_clients = []  # List of users


# I added listen_for_messages Function. This function runs in a separate thread for each client. It continuously listens for messages from a specific client, and when a non-empty message is received, it appends the sender's username and forwards the message to all connected clients.

    def listen_for_messages(client, username):
        while True:
            try:
                message = client.recv(2048).decode('utf-8')
                if message != '':
                    final_msg = username + '-' + message
                    send_messages_to_all(username, final_msg)
                else:
                    print("The message sent from the client is empty")
            except Exception as e:
                print(f"Error receiving message: {e}")
                break


# Next is send_message_to_clients Function. This function sends a message to the clients by encoding the message and using sendall to ensure that the entire message is sent.

    def send_message_to_clients(client, message):
        client.sendall(message.encode())


# Also added send_messages_to_all Function. This function sends a message to all connected clients except the sender. It iterates over active_clients and uses the send_message_to_clients function to send the message to each client.

    def send_messages_to_all(from_username, message):
        for user in active_clients:
            send_message_to_clients(user[1], message)


# Then client_handler Function. This function handles the initial connection from a client. It receives the client's username, adds the client to the active_clients list, sends a prompt message to all clients about the new connection, and then starts a new thread to listen for messages from this client.
# Function to handle a client

    def client_handler(client):
        while True:
            try:
                username = client.recv(2048).decode('utf-8')
                if username != '':
                    active_clients.append((username, client))
                    prompt_message = "SERVER-" + f"{username} added to the chat"
                    send_messages_to_all("SERVER", prompt_message)
                    break
                else:
                    print("Client username is empty")
                    
            except Exception as e:
                print(f"Error receiving username: {e}")
                break'
                
        threading.Thread(target=listen_for_messages, args=(client, username,)).start()


# After that is the main Function. The main function initializes the server socket, binds it to the specified host and port, and starts listening for incoming connections. When a connection is accepted, it prints a success message and starts a new thread to handle that client.

    def main():
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            server.bind((HOST, PORT))
            print(f"Running the server on {HOST} {PORT}")
        except Exception as e:
            print(f"Unable to bind to host {HOST} and port {PORT}\nError: {e}")
        return
        
        server.listen(LISTENER_LIMIT)
        while True:
            client, address = server.accept()
            print(f"Succesfully connected to client {address[0]} {address[1]}")
            
        threading.Thread(target=client_handler, args=(client,)).start()

        
# Then lastly the if name == '__main__': Block. This block ensures that the main function is called only if the script is executed directly

    if __name__ == '__main__':

        main()

# The second thing to create is the client and then imports the necessary modules such as socket for network communication, threading for handling multiple tasks concurrently, and tkinter for creating the GUI. scrolledtext and messagebox are specific components of tkinter used for displaying scrollable text and message dialogs, respectively.
    import socket
    import threading
    import tkinter as tk
    from tkinter import scrolledtext, messagebox

# Next is to define the host IP address and port number.
# The host is the standard loopback interface address (localhost)
# The port is to listen on (non-privileged ports are > 1023)
    HOST = '192.168.1.127'
    PORT = 1234

 # Create Constants for color codes, and font specifications for the GUI.
    MEDIUM_GREY = '#1F1B24'
    OCEAN_BLUE = '#00B2FF'
    WHITE = "white"
    FONT = ("Helvetica", 17)
    BUTTON_FONT = ("Helvetica", 15)
    SMALL_FONT = ("Helvetica", 13)

# Then the Socket Initialization. A socket is created using the socket module for establishing a connection to the server.
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
# Next is to create Event Handling Functions. 

# add_message(message) - Appends a message to the scrolled text widget, enabling automatic scrolling to the bottom.    
    def add_message(message):
        message_box.config(state=tk.NORMAL)
        message_box.insert(tk.END, message + '\n')
        message_box.config(state=tk.DISABLED)
        message_box.yview(tk.END)  # Auto-scroll to the bottom
    
# connect() - Attempts to connect to the server, sends the username to the server, and starts a thread to listen for messages from the server.
    def connect():
        try:
            client.connect((HOST, PORT))
            print("Successfully connected to the server")
            add_message("[SERVER] Successfully connected to the server")
        except Exception as e:
            messagebox.showerror("Unable to connect to server", f"Unable to connect to server {HOST} {PORT}\nError: {e}")
            return
    
        username = username_textbox.get()
        if username != '':
            client.sendall(username.encode())
        else:
            messagebox.showerror("Invalid username", "Username cannot be empty")
            return
    
        threading.Thread(target=listen_for_messages_from_server, args=(client,)).start()
    
        username_textbox.config(state=tk.DISABLED)
        username_button.config(state=tk.DISABLED)
    
# send_message() - Sends the entered message to the server.  
    def send_message():
        message = message_textbox.get()
        if message != '':
            client.sendall(message.encode())
            message_textbox.delete(0, tk.END)
        else:
            messagebox.showerror("Empty Message", "Message cannot be empty")
            
# setup the GUI of the app. 
    # Design
    root = tk.Tk()
    root.geometry("600x600")
    root.title("Simple Real-Time Chat-App")
    root.resizable(False, False)
    
    root.grid_rowconfigure(0, weight=1)
    root.grid_rowconfigure(1, weight=4)
    root.grid_rowconfigure(2, weight=1)
    
    top_frame = tk.Frame(root, width=600, height=100, bg=MEDIUM_GREY)
    top_frame.grid(row=0, column=0, sticky=tk.NSEW)
    
    middle_frame = tk.Frame(root, width=600, height=400, bg=MEDIUM_GREY)
    middle_frame.grid(row=1, column=0, sticky=tk.NSEW)
    
    bottom_frame = tk.Frame(root, width=600, height=100, bg=MEDIUM_GREY)
    bottom_frame.grid(row=2, column=0, sticky=tk.NSEW)
    
# Next is the username label, textbox, button and message box and textbox for the app.
    username_label = tk.Label(top_frame, text="Enter username:", font=FONT, bg=MEDIUM_GREY, fg=WHITE)
    username_label.pack(side=tk.LEFT, padx=10)
    
    username_textbox = tk.Entry(top_frame, font=FONT, bg=MEDIUM_GREY, fg=WHITE, width=23)
    username_textbox.pack(side=tk.LEFT)
    
    username_button = tk.Button(top_frame, text=" Join ", font=BUTTON_FONT, bg=OCEAN_BLUE, fg=WHITE, command=connect)
    username_button.pack(side=tk.LEFT, padx=25)
    
    message_textbox = tk.Entry(bottom_frame, font=FONT, bg=MEDIUM_GREY, fg=WHITE, width=38)
    message_textbox.pack(side=tk.LEFT, padx=5)
    
    message_button = tk.Button(bottom_frame, text="Send", font=BUTTON_FONT, bg=OCEAN_BLUE, fg=WHITE, command=send_message)
    message_button.pack(side=tk.LEFT, padx=15)
    
    message_box = scrolledtext.ScrolledText(middle_frame, font=SMALL_FONT, bg=MEDIUM_GREY, fg=WHITE, width=67, height=26.5)
    message_box.config(state=tk.DISABLED)
    message_box.pack(side=tk.TOP)

# listen_for_messages_from_server(client) - Listens for incoming messages from the server in a separate thread.
    def listen_for_messages_from_server(client):
        while True:
            try:
                message = client.recv(2048).decode('utf-8')
                if message != '':
                    # Splitting the message
                    username, content = message.split("-", 1)
                    add_message(f"[{username}] {content}")
                else:
                    messagebox.showerror("Error", "Message received from the server is empty")
            except Exception as e:
                print(f"Error receiving message: {e}")
                break

# Lastly the Main Loop.  The main function starts the tkinter main loop, and the main block ensures that the main function is called when the script is run.
    def main():
        root.mainloop()
    
    if __name__ == '__main__':
        main()
