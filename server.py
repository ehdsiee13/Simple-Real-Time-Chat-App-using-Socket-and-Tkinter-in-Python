import socket
import threading

HOST = '192.168.1.127'
PORT = 1234
LISTENER_LIMIT = 5
active_clients = []  # List of users


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


def send_message_to_clients(client, message):
    client.sendall(message.encode())


def send_messages_to_all(from_username, message):
    for user in active_clients:
        send_message_to_clients(user[1], message)


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


if __name__ == '__main__':
    main()