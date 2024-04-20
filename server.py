import socket
import threading

# Connection Data
host = '127.0.0.1'
port = 55556

# Starting the Server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

# List for Clients and their Nicknames
clients = []        # List to store client sockets
nicknames = []      # List to store client nicknames


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
            msg = message = client.recv(1024)     # Receive the message from the client
            if msg.decode('ascii').startswith('KICK'):
                # Kick a user if the sender is the admin
                if nicknames[clients.index(client)] == 'admin':
                    name_to_kick = msg.decode('ascii')[5:]
                    kick_user(name_to_kick)
                else:
                    client.send('Command was refused'.encode('ascii'))
            elif msg.decode('ascii').startswith('BAN'):
                # Ban a user if the sender is the admin
                if nicknames[clients.index(client)] == 'admin':
                    name_to_ban = msg.decode('ascii')[4:]
                    kick_user(name_to_ban)      # Kick the user first
                    with open('bans.txt', 'a') as f:
                        f.write(f'{name_to_ban}\n')     # Add user to banlist
                    print(f'{name_to_ban} was banned!')
                else:
                    client.send('Command was refused'.encode('ascii'))
            else:
                broadcast(message)      # Broadcast the message to all clients
        except:
            # Removing and Closing Clients
            if client in clients:
                index = clients.index(client)
                clients.remove(client)
                client.close()
                nickname = nicknames[index]
                broadcast(f"{nickname} left the chat".encode('ascii'))  # Inform all clients
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
        client.send('NICK'.encode('ascii'))     # Request client to send its nickname
        nickname = client.recv(1024).decode('ascii')   # Receive and decode the nickname

        # Check if the client is banned
        with open('bans.txt', 'r') as f:
            bans = f.readlines()
        if nickname+'\n' in bans:
            client.send('BAN'.encode('ascii'))     # Inform the client that it's banned
            client.close()
            continue

        # Authenticate admin user
        if nickname == 'admin':
            client.send('PASS'.encode('ascii'))     # Request admin password
            password = client.recv(1024).decode('ascii')   # Receive and decode password
            if password != 'admin-pass':
                client.send('REFUSE'.encode('ascii'))    # Refuse connection if password is incorrect
                client.close()
                continue

        nicknames.append(nickname)      # Add nickname to the list
        clients.append(client)          # Add client socket to the list

        # Print and Broadcast Nickname
        print(f'Nickname of the Client is {nickname}!')
        broadcast(f"{nickname} joined the chat!".encode('ascii'))  # Inform all clients
        client.send("Connected to the Server!".encode('ascii'))     # Confirm connection to the client

        # Start Handling Thread For Client
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


def kick_user(name):
    """Kick a user from the chat."""
    if name in nicknames:
        name_index = nicknames.index(name)
        client_to_kick = clients[name_index]
        clients.remove(client_to_kick)     # Remove the client from the list
        client_to_kick.send("You were kicked by an admin".encode('ascii'))   # Inform the kicked client
        client_to_kick.close()      # Close the connection
        nicknames.remove(name)      # Remove nickname from the list
        broadcast(f'{name} was kicked by an admin!'.encode('ascii'))     # Inform all clients


print("Server is listening...")
receive()   # Start receiving and handling connections
