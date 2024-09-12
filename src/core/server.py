import socket
from typing import Any

from src.core.utils import (
    LOCAL_HOST, LOCAL_PORT
)
from src.core.debug import *

class ServerClient_:
    """
    Represents a client connected to the server.

    Attributes:
        port (int): The port number of the client.
        host (str): The host address of the client.
        name (str): The name of the client.
        obj (socket.socket | None): The socket object for the client connection.
        id (int | None): The unique identifier for the client.
    """

    def __init__(self, port: int, host: str, name: str, id: int | None = None, obj: socket.socket | None = None):
        """
        Initialize a ServerClient_ instance.

        Args:
            port (int): The port number of the client.
            host (str): The host address of the client.
            name (str): The name of the client.
            id (int | None, optional): The unique identifier for the client. Defaults to None.
            obj (socket.socket | None, optional): The socket object for the client connection. Defaults to None.
        """
        self.port = port
        self.host = host
        self.name = name
        self.obj = obj
        self.id = id
        

class Server:
    """
    Represents a server that can accept and manage client connections.

    Attributes:
        host (str): The host address of the server.
        port (int): The port number of the server.
        server (socket.socket): The server socket object.
        clients (list[ServerClient_]): A list of connected clients.
    """

    def __init__(self, host=LOCAL_HOST, port=LOCAL_PORT):
        """
        Initialize a Server instance.

        Args:
            host (str, optional): The host address of the server. Defaults to LOCAL_HOST.
            port (int, optional): The port number of the server. Defaults to LOCAL_PORT.

        Raises:
            Exception: If the server cannot be created and bound to the specified host and port.
        """
        self.host = host
        self.port = port
        try:
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server.bind((self.host, self.port))
            self.server.listen(5)
            LogServerCreated(self.port, self.host)
        except:
            LogServerNotCreated(self.port, self.host)
        self.clients: list[ServerClient_] = []


    def listen_(self):
        """
        Start listening for incoming client connections.

        This method runs in an infinite loop, accepting new client connections
        and adding them to the list of connected clients.

        Note:
            This method will run indefinitely until the server is stopped externally.
        """
        LogServerStartListening()
        while True:
            client, address = self.server.accept()
            name_and_id = client.recv(1024).decode()
            name, id = name_and_id.split("|")
            self.clients.append(ServerClient_(address[1], address[0], name, id, client))
            LogClientConnectToServer(address[1], address[0], name, id)
