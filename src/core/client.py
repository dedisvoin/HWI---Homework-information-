import socket

from src.core.utils import (
    LOCAL_HOST, LOCAL_PORT
)

from src.core.debug import *
from ast import literal_eval

class Client:
    """
    A client class for establishing socket connections and communication.

    This class provides functionality to create a socket connection, connect to a server,
    send and receive string data over the established connection.

    Attributes:
        host (str): The host address to connect to. Defaults to LOCAL_HOST.
        port (int): The port number to connect to. Defaults to LOCAL_PORT.
        socket (socket.socket): The socket object used for communication.
    """

    def __init__(self, host=LOCAL_HOST, port=LOCAL_PORT):
        """
        Initialize a new Client instance.

        Args:
            host (str, optional): The host address to connect to. Defaults to LOCAL_HOST.
            port (int, optional): The port number to connect to. Defaults to LOCAL_PORT.

        Raises:
            LogClientNotCreated: If the socket creation fails.
        """
        self.host = host
        self.port = port
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            LogClientCreated(self.host, self.port)
        except:
            LogClientNotCreated(self.host, self.port)
    
    def connect_(self):
        """
        Attempt to establish a connection to the specified host and port.

        Raises:
            LogClientNotConnected: If the connection attempt fails.
        """
        try:
            self.socket.connect((self.host, self.port))
            LogClientConnected(self.host, self.port)
        except:
            LogClientNotConnected(self.host, self.port)

    def send_string_(self, string: str):
        """
        Send a string over the established connection.

        Args:
            string (str): The string to be sent.

        Note:
            This method silently fails if an exception occurs during sending.
        """
        try:
            self.socket.send(string.encode())
        except: ...

    def recv_string_(self, buffer_size: int = 1024):
        """
        Receive a string from the established connection.

        Args:
            buffer_size (int, optional): The maximum amount of data to be received at once.
                Defaults to 1024 bytes.

        Returns:
            str: The received string, or None if an exception occurs.

        Note:
            This method silently fails and returns None if an exception occurs during receiving.
        """
        try:
            return self.socket.recv(buffer_size).decode()
        except: ...