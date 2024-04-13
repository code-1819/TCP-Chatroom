---

# TCP Chatroom

TCP Chatroom is a simple chat application implemented using Python's socket programming. It allows multiple clients to connect to a central server and communicate with each other in real-time.

## Features

- **Real-time Chat**: Multiple clients can connect to the server and chat with each other in real-time.
- **Nickname Support**: Clients can choose their nicknames, which are displayed alongside their messages.
- **Robust Connection Handling**: The server gracefully handles client connections and disconnections.

## Getting Started

### Prerequisites

- Python 3.x

### Usage

1. Clone the repository:

    ```bash
    git clone https://github.com/your_username/tcp-chatroom.git
    ```

2. Run the server:

    ```bash
    python server.py
    ```

3. Run one or more clients:

    ```bash
    python client.py
    ```

4. Choose a nickname for each client when prompted.

5. Start chatting!

## How It Works

### Server (`server.py`)

1. The server listens for incoming connections on a specified host and port.
2. Upon connection, it requests the client's nickname and broadcasts it to all connected clients.
3. It continuously listens for messages from clients and broadcasts them to all other clients.

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
