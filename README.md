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
            break
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
