---

# GUI TCP Chatroom

GUI Chatroom is a simple chat application implemented using Python's socket programming. It allows multiple clients to connect to a central server and communicate with each other in real-time.

## Getting Started

### Prerequisites

- Python 3.x

### Usage

1. Clone the repository:

    ```bash
    git clone https://github.com/code-1819/TCP-Chatroom.git
    ```

2. Navigate to the CLI Chatroom Directory

   ```bash
   cd GUI Chatroom
   ```

3. Run the server:

    ```bash
    python server.py
    ```

4. Run one or more clients:

    ```bash
    python client.py
    ```

5. Choose a nickname for each client when prompted.

6. Start chatting!

    
## How It Works

### Server (`server.py`)

1. The server listens for incoming connections on a specified host and port.
2. Upon connection, it requests the client's nickname and broadcasts it to all connected clients.
3. It continuously listens for messages from clients and broadcasts them to all other clients.
4. It supports admin commands like kicking and banning users.

### Client (`client.py`)

1. The client connects to the server.
2. It chooses a nickname and sends it to the server.
3. It continuously listens for messages from the server and displays them to the user.
4. It allows the user to input messages and sends them to the server for broadcasting.

## Contributing

Contributions are welcome! If you'd like to improve this project, please fork the repository and submit a pull request with your changes.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---
