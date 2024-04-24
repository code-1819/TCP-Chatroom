import socket
import threading

# Connection Data
host = '127.0.0.1'
port = 9090

# Starting the Server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

# List for Clients and their Nicknames
clients = []  # List to store client sockets
nicknames = []  # List to store client nicknames


# Sending Messages To All Connected Clients
def broadcast(message):
    """Send a message to all connected clients."""
    for client in clients:
        client.send(message)


# Handling Messages From Clients
def handle(client):
    """Handle messages from a single client."""
    while True:
        try:
            # Broadcasting Messages
            message = client.recv(1024)  # Receive the message from the client
            print(f"{nicknames[clients.index(client)]} says {message}")
            broadcast(message)  # Broadcast the message to all clients
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            nicknames.remove(nickname)
            break


# Receiving / Listening Function
def receive():
    """Accept incoming connections and handle them."""
    while True:
        # Accept Connection
        client, address = server.accept()
        print(f"Connected with {str(address)}")

        # Request and Store Nickname
        client.send('NICK'.encode('utf-8'))  # Request client to send its nickname
        nickname = client.recv(1024).decode('utf-8')  # Receive and decode the nickname

        nicknames.append(nickname)  # Add nickname to the list
        clients.append(client)  # Add client socket to the list

        # Print and Broadcast Nickname
        print(f'Nickname of the Client is {nickname}!')
        broadcast(f"{nickname} joined the chat!\n".encode('utf-8'))  # Inform all clients
        client.send("Connected to the Server!".encode('utf-8'))  # Confirm connection to the client

        # Start Handling Thread For Client
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


print("Server is listening...")
receive()  # Start receiving and handling connections
