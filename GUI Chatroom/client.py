import socket
import threading
import tkinter
import tkinter.scrolledtext
from tkinter import simpledialog

# Server connection details
HOST = '127.0.0.1'
PORT = 9090


class Client:
    """Client class for handling GUI chat functionality."""

    def __init__(self, host, port):
        """Initialize the client."""
        # Create a socket for communication
        self.send_button = None
        self.input_area = None
        self.msg_label = None
        self.chat_label = None
        self.text_area = tkinter.scrolledtext.ScrolledText(self.win)
        self.win = None
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Connect to the server
        self.sock.connect((host, port))

        # Create a tkinter window for the GUI
        msg = tkinter.Tk()
        msg.withdraw()

        # Prompt the user to choose a nickname
        self.nickname = simpledialog.askstring("Nickname", "Please choose a nickname", parent=msg)

        # Flags for GUI status and client running state
        self.gui_done = False
        self.running = True

        # Create threads for GUI loop and message receiving
        gui_thread = threading.Thread(target=self.gui_loop)
        receive_thread = threading.Thread(target=self.receive)

        # Start the threads
        gui_thread.start()
        receive_thread.start()

    def gui_loop(self):
        """GUI loop for creating and managing the tkinter window."""
        # Create the tkinter window
        self.win = tkinter.Tk()
        self.win.configure(bg="lightgray")

        # Create and configure GUI elements
        self.chat_label = tkinter.Label(self.win, text="Chat:", bg="lightgray")
        self.chat_label.config(font=("Arial", 12))
        self.chat_label.pack(padx=20, pady=5)

        self.text_area.pack(padx=20, pady=5)
        self.text_area.config(state='disabled')

        self.msg_label = tkinter.Label(self.win, text="Message:", bg="lightgray")
        self.msg_label.config(font=("Arial", 12))
        self.msg_label.pack(padx=20, pady=5)

        self.input_area = tkinter.Text(self.win, height=3)
        self.input_area.pack(padx=20, pady=5)

        self.send_button = tkinter.Button(self.win, text="Send", command=self.write)
        self.send_button.config(font=("Arial", 12))
        self.send_button.pack(padx=20, pady=5)

        # Set GUI status flag
        self.gui_done = True

        # Handle window closure
        self.win.protocol("WM_DELETE_WINDOW", self.stop)

        # Start the GUI event loop
        self.win.mainloop()

    def write(self):
        """Send a message to the server."""
        # Construct the message
        message = f"{self.nickname}: {self.input_area.get('1.0', 'end')}"
        # Send the message to the server
        self.sock.send(message.encode('utf-8'))
        # Clear the input area
        self.input_area.delete('1.0', 'end')

    def stop(self):
        """Stop the client."""
        # Set running flag to False
        self.running = False
        # Close the socket connection
        self.sock.close()
        # Check if the tkinter window exists
        if hasattr(self, 'win'):
            # Close the tkinter window
            self.win.destroy()
        # Exit the program
        exit(0)

    def receive(self):
        """Receive messages from the server."""
        while self.running:
            try:
                # Receive a message from the server
                message = self.sock.recv(1024).decode('utf-8')
                # If the message is a nickname request
                if message.startswith('NICK'):
                    # Send the nickname to the server
                    self.sock.send(self.nickname.encode('utf-8'))
                # If the message is a regular chat message
                else:
                    # If the GUI is initialized
                    if self.gui_done:
                        # Enable the text area, insert the message, and scroll to the end
                        self.text_area.config(state='normal')
                        self.text_area.insert('end', message)
                        self.text_area.yview('end')
                        self.text_area.config(state='disabled')
            except ConnectionAbortedError:
                break
            except ConnectionResetError:
                print("Connection with server reset.")
                # Stop the client
                self.stop()
                break
            except OSError as e:
                print("Error:", e)
                # Stop the client
                self.stop()
                break


# Create a Client instance
client = Client(HOST, PORT)
