import socket
import threading

# Choosing Nickname
nickname = input("Choose a Nickname: ")
if nickname == 'admin':
    password = input("Enter password for admin: ")

# Connecting to Server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 55556))

stop_thread = False


# Listening to Server and Sending Nickname
def receive():
    """
    Listen for messages from the server.
    Handles the initial exchange of nickname and, if applicable, password.
    """
    while True:
        global stop_thread
        if stop_thread:
            break
        try:
            # Receive Message From Server
            message = client.recv(1024).decode('ascii')
            if message == 'NICK':
                # Send Nickname to the server
                client.send(nickname.encode('ascii'))
                # Receive the next message from the server
                next_message = client.recv(1024).decode('ascii')
                if next_message == 'PASS':
                    # If password authentication is required, send password
                    client.send(password.encode('ascii'))
                    # Check if connection is refused due to the wrong password
                    if client.recv(1024).decode('ascii') == 'REFUSE':
                        print("Connection was refused! Wrong Password!")
                        stop_thread = True
                elif next_message == 'BAN':
                    # Inform the user if connection is refused due to ban
                    print('Connection refused because of a ban!')
                    client.close()
                    stop_thread = True
            else:
                # Print the received message from the server
                print(message)
        except:
            # Close Connection When Error
            print("An Error occurred!")
            client.close()
            break


# Sending Messages To Server
def write():
    """Send messages to the server."""
    while True:
        if stop_thread:
            break
        message = f'{nickname}: {input("")}'
        if message[len(nickname)+2:].startswith('/'):
            if nickname == 'admin':
                if message[len(nickname)+2:].startswith('/kick'):
                    # Send a command to kick a user
                    client.send(f'KICK {message[len(nickname)+2+6:]}'.encode('ascii'))
                elif message[len(nickname)+2:].startswith('/ban'):
                    # Send a command to ban a user
                    client.send(f'BAN {message[len(nickname)+2+5:]}'.encode('ascii'))
            else:
                # Inform the user that only admins can execute commands
                print("Commands can only be executed by an admin!")
        else:
            # Send the normal message to the server
            client.send(message.encode('ascii'))


# Starting Threads For Listening And Writing
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
