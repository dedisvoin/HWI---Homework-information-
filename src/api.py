"""
This module contains classes and functions for handling client-server communication and database operations.

Imports:
    time: For sleep function
    src.core: For client, server, utils, and database modules
    src.core.debug: For logging functions
    ast: For literal_eval function
    threading: For Thread class
    uuid: For generating unique identifiers

Classes:
    Requests: Contains class methods for different types of requests
    IDZClient: Client class for sending requests and receiving data
    IDZServer: Server class for handling client requests and database operations

Functions:
    get_request_type: Extracts the request type from a request command
"""

from time import sleep
from src.core import client
from src.core.debug import *
from src.core import server
from src.core import utils
from src.core import database

from src.core.database import INT, TEXT

from ast import literal_eval

from threading import Thread

import uuid

class Requests:
    """
    A class containing class methods for different types of requests.
    """

    @classmethod
    def GET_ALL(self):
        """
        Returns a request string for getting all data.

        Returns:
            str: The request string for getting all data.
        """
        return 'GETALL*end'
    
    @classmethod
    def ADD_INFO(self, info: list):
        """
        Returns a function that generates a request string for adding information.

        Args:
            info (list): A list containing [user, lesson, date, wait_date, text].

        Returns:
            function: A function that returns the request string for adding information.
        """
        def inner():
            return f'ADDINFO*{info}end'
        return inner
    
    @classmethod
    def GET_FOR_DATE(self, data: str):
        """
        Returns a function that generates a request string for getting data for a specific date.

        Args:
            data (str): The date to retrieve data for.

        Returns:
            function: A function that returns the request string for getting data for a specific date.
        """
        def inner():
            return f'GETFORDATE*{data}end'
        return inner
    
    @classmethod
    def GET_FOR_WAIT_DATE(self, data: str):
        """
        Returns a function that generates a request string for getting data for a specific wait date.

        Args:
            data (str): The wait date to retrieve data for.

        Returns:
            function: A function that returns the request string for getting data for a specific wait date.
        """
        def inner():
            return f'GETFORWAITDATE*{data}end'
        return inner
    
    @classmethod
    def DELETE_INFO(self, user_name: str, date: str):
        """
        Returns a function that generates a request string for deleting information.
        Args:
            user_name (str): The name of the user.
            date (str): The date to delete information for.

        Returns:
            function: A function that returns the request string for deleting information.
        """
        def inner():
            return f'DELETEINFO*{user_name}~{date}end'
        return inner
    
    @classmethod
    def DELETE_ALL(self):
        """
        Returns a function that generates a request string for deleting all data.
        Returns:
            function: A function that returns the request string for deleting all data.
        """
        def inner():
            return f'DELETEALL*end'
        return inner
        
        
    
def get_request_type(request_command: str) -> str:
    """
    Extracts the request type from a request command.

    Args:
        request_command (str): The full request command.

    Returns:
        str: The request type.
    """
    return request_command.split('*')[0]

class HWIClient(client.Client):
    """
    A client class for sending requests and receiving data.

    Attributes:
        name (str): The name of the client.
        id (uuid.UUID): A unique identifier for the client.
    """

    def __init__(self, host: str = utils.LOCAL_HOST, port: int = utils.LOCAL_PORT, name: str = "Unnamed"):
        """
        Initializes the IDZClient.

        Args:
            host (str): The host address. Defaults to utils.LOCAL_HOST.
            port (int): The port number. Defaults to utils.LOCAL_PORT.
            name (str): The name of the client. Defaults to "Unnamed".
        """
        super().__init__(host, port)
        self.name = name
        self.id = uuid.uuid4()

    def connect(self):
        """
        Connects to the server and sends the client's name and ID.
        """
        self.connect_()
        self.send_string_(f'{self.name}|{self.id}')

    def wait_data(self, buffer_size: int = 1024*15):
        """
        Waits for and receives data from the server.

        Args:
            buffer_size (int): The size of the receive buffer. Defaults to 1024.

        Returns:
            Any: The received data, parsed using literal_eval.
        """
        data = ''
        while data == '':
            data = self.socket.recv(buffer_size).decode()
            string = literal_eval(data)
        return string

    def request(self, request: Requests):
        """
        Sends a request to the server and waits for a response if applicable.

        Args:
            request (Requests): The request to send.

        Returns:
            Any: The response data if the request is "getable", None otherwise.
        """
        command = request()
        self.send_string_(command)

        # if request getable
        if 'GETALL' in command:
            return self.wait_data()
        if 'GETFORDATE' in command:
            return self.wait_data()
        if 'GETFORWAITDATE' in command:
            return self.wait_data()
        if 'DELETEINFO' in command:
            return self.wait_data()
        if 'DELETEALL' in command:
            return self.wait_data()


class HWIServer(server.Server):
    """
    A server class for handling client requests and database operations.

    Attributes:
        data_base_connect: The database connection object.
        data_base_cursor: The database cursor object.
        requests (list): A list to store incoming requests.
    """

    def __init__(self, host: str = utils.LOCAL_HOST, port: int = utils.LOCAL_PORT):
        """
        Initializes the IDZServer.

        Args:
            host (str): The host address. Defaults to utils.LOCAL_HOST.
            port (int): The port number. Defaults to utils.LOCAL_PORT.
        """
        super().__init__(host, port)
        self.data_base_connect = None
        self.data_base_cursor = None
        self.requests = []

    def clean_data_base(self) -> list[str]:
        """
        Cleans the database by deleting all data.
        """
        self.create_data_base()
        info = database.execute_delete_all(self.data_base_cursor, self.data_base_connect, 'Tasks')
        return info

    def create_data_base(self):
        """
        Creates or connects to the database and initializes the cursor.
        """
        try:
            self.data_base_connect = database.connect('tasks.db')
            self.data_base_cursor = database.get_cursor(self.data_base_connect)

        except:
            database.create('tasks.db')
            self.data_base_connect = database.connect('tasks.db')
            database.execute_table_create(database.get_cursor(self.data_base_connect), self.data_base_connect, 'Tasks', 
                                        ['user','user_id','lesson', 'date', 'wait_date', 'text'],
                                        [TEXT, TEXT, TEXT, TEXT, TEXT, TEXT]
            )
            self.data_base_cursor = database.get_cursor(self.data_base_connect)

    def wait_requests_(self, buffer_size: int = 1024, tick: int | float = 0.8):
        """
        Continuously listens for incoming requests from clients.

        Args:
            buffer_size (int): The size of the receive buffer. Defaults to 1024.
            tick (int | float): The time to sleep between checks. Defaults to 0.8.
        """
        while True:
            sleep(tick)
            for client in self.clients:
                try:
                    command = client.obj.recv(buffer_size).decode()
                    if 'end' in command:
                        command = command.split('end')[0]
                    if command != '':
                        LogRecuestRecved(command)
                        self.requests.append(f'{command}|{client.id}')
                except:...

    def request_add_info(self, request: str, client_id: str):
        """
        Handles the request to add information to the database.

        Args:
            request (str): The request string containing the information to add.
            client_id (str): The ID of the client making the request.
        """
        self.create_data_base()
        info: list = literal_eval(request.split('*')[1])
        info.insert(1, str(client_id))
        database.execute_add_info(
            self.data_base_cursor,
            self.data_base_connect,
            'Tasks',
            info
        )
        LogInformationAdded(info)

    def get_client_by_id(self, client_id: str):
        """
        Retrieves a client object by its ID.

        Args:
            client_id (str): The ID of the client to retrieve.

        Returns:
            Client: The client object if found, None otherwise.
        """
        for client in self.clients:
            if client.id == client_id:
                return client

    def request_get_all(self, request: str, client_id: str):
        """
        Handles the request to get all information from the database.

        Args:
            request (str): The request string.
            client_id (str): The ID of the client making the request.
        """
        self.create_data_base()
        info = database.execute_get_all_info(self.data_base_cursor, self.data_base_connect, 'Tasks')
        client = self.get_client_by_id(client_id)
        client.obj.send(f'{info}'.encode())

    def request_get_for_data(self, request: str, client_id: str):
        """
        Handles the request to get information for a specific date.

        Args:
            request (str): The request string containing the date.
            client_id (str): The ID of the client making the request.
        """
        self.create_data_base()
        info = database.execute_get_all_info(self.data_base_cursor, self.data_base_connect, 'Tasks')
        return_data = []

        date = request.split('*')[1]
        for inf in info:
            if inf[3] == date:
                return_data.append(inf)
        LogInformationGetedForDate(date, client_id)
        client = self.get_client_by_id(client_id)
        client.obj.send(f'{return_data}'.encode())

    def request_get_for_wait_date(self, request: str, client_id: str):
        """
        Handles the request to get information for a specific wait date.

        Args:
            request (str): The request string containing the wait date.
            client_id (str): The ID of the client making the request.
        """
        self.create_data_base()
        info = database.execute_get_all_info(self.data_base_cursor, self.data_base_connect, 'Tasks')
        return_data = []

        date = request.split('*')[1]
        for inf in info:
            if inf[4] == date:
                return_data.append(inf)
        client = self.get_client_by_id(client_id)
        client.obj.send(f'{return_data}'.encode())

    def request_delete_info(self, request: str, client_id: str):
        """
        Handles the request to delete information from the database.
        Args:
            request (str): The request string containing the information to delete.
            client_id (str): The ID of the client making the request.
        """
        name, date = request.split('*')[1].split('~')
        self.create_data_base()
        info = database.execute_delete_info(
            self.data_base_cursor,
            self.data_base_connect,
            'Tasks',
            name,
            date
        )
        print(info)
        client = self.get_client_by_id(client_id)
        client.obj.send(f'{info}'.encode())

    def request_delete_all(self, request: str, client_id: str):
        """
        Handles the request to delete all information from the database.
        Args:
            request (str): The request string.
            client_id (str): The ID of the client making the request.
        """
        self.create_data_base()
        info = database.execute_delete_all(self.data_base_cursor, self.data_base_connect, 'Tasks')
        
        client = self.get_client_by_id(client_id)
        client.obj.send(f'{info}'.encode())

    

    def request_parse_(self):
        """
        Continuously parses and handles incoming requests.
        """
        while True:
            
            if len(self.requests) > 0:
                request = self.requests.pop(0)
                command, client_id = request.split('|')
               
               
                if get_request_type(command) == 'GETALL':
                    self.request_get_all(command, client_id)
                if get_request_type(command) == 'ADDINFO':
                    self.recuest_add_info(command, client_id)
                if get_request_type(command) == 'GETFORDATE':
                    self.request_get_for_data(command, client_id)
                if get_request_type(command) == 'GETFORWAITDATE':
                    self.request_get_for_wait_date(command, client_id)
                if get_request_type(command) == 'DELETEINFO':
                    self.request_delete_info(command, client_id)
                if get_request_type(command) == 'DELETEALL':
                    self.request_delete_all(command, client_id)
                
    def run(self):
        """
        Starts the server by running the listen, wait_requests, and request_parse methods in separate threads.
        """
        Thread(target=self.listen_).start()
        Thread(target=self.wait_requests_).start()
        Thread(target=self.request_parse_).start()
