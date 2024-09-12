from colorama import Fore

# Define color-coded log prefixes
LOG = f'[ {Fore.CYAN}log{Fore.RESET} ]'
SERVER = f'[ {Fore.YELLOW}server{Fore.RESET} ]'
CLIENT = f'[ {Fore.GREEN}client{Fore.RESET} ]'
DATABASE = f'[ {Fore.RED}database{Fore.RESET} ]'

# Define color-coded yes/no indicators
YES = f'{Fore.GREEN} [ yes ] {Fore.RESET}'
NO = f'{Fore.RED} [ no ] {Fore.RESET}'

def LogServerCreated(port: int, host: str) -> None:
    """
    Log a message indicating that a server has been created.

    Args:
        port (int): The port number on which the server is created.
        host (str): The host address of the server.

    Returns:
        None
    """
    print(f"{LOG} {SERVER} Server created on {host}:{port} {YES}")

def LogServerNotCreated(port: int, host: str) -> None:
    """
    Log a message indicating that a server could not be created and exit the program.

    Args:
        port (int): The port number on which the server creation was attempted.
        host (str): The host address where the server creation was attempted.

    Returns:
        None
    """
    print(f"{LOG} {SERVER} Server not created on {host}:{port} {NO}")
    exit(-1)

def LogServerStarted(port: int, host: str) -> None:
    """
    Log a message indicating that a server has started.

    Args:
        port (int): The port number on which the server is running.
        host (str): The host address of the server.

    Returns:
        None
    """
    print(f"{LOG} {SERVER} Server started on {host}:{port} {YES}")

def LogServerStartListening() -> None:
    """
    Log a message indicating that the server has started listening for connections.

    Returns:
        None
    """
    print(f"{LOG} {SERVER} Server started listening...")

def LogClientCreated(port: int, host: str) -> None:
    """
    Log a message indicating that a client has been created.

    Args:
        port (int): The port number associated with the client.
        host (str): The host address associated with the client.

    Returns:
        None
    """
    print(f"{LOG} {SERVER} Client created! {YES}")

def LogClientNotCreated(port: int, host: str) -> None:
    """
    Log a message indicating that a client could not be created and exit the program.

    Args:
        port (int): The port number associated with the client creation attempt.
        host (str): The host address associated with the client creation attempt.

    Returns:
        None
    """
    print(f"{LOG} {SERVER} Client not created. {NO}")
    exit(-1)

def LogClientConnected(port: int, host: str) -> None:
    """
    Log a message indicating that a client has connected to a server.

    Args:
        port (int): The port number to which the client is connected.
        host (str): The host address to which the client is connected.

    Returns:
        None
    """
    print(f"{LOG} {SERVER} Client connected to {host}:{port} {YES}")

def LogClientNotConnected(port: int, host: str) -> None:
    """
    Log a message indicating that a client could not connect to a server and exit the program.

    Args:
        port (int): The port number to which the client attempted to connect.
        host (str): The host address to which the client attempted to connect.

    Returns:
        None
    """
    print(f"{LOG} {SERVER} Client not connected to {host}:{port} {NO}")
    exit(-1)

def LogClientConnectToServer(port: int, host: str, name: str, id: str) -> None:
    """
    Log a message indicating that a specific client has connected to a server.

    Args:
        port (int): The port number to which the client is connected.
        host (str): The host address to which the client is connected.
        name (str): The name of the client.
        id (str): The unique identifier of the client.

    Returns:
        None
    """
    print(f"{LOG} {SERVER} Client '{name}' (id: {id}) connected! ip {host}:{port} {YES}")

def LogDataBaseCreated(name: str) -> None:
    """
    Log a message indicating that a database has been created.

    Args:
        name (str): The name of the created database.

    Returns:
        None
    """
    print(f"{LOG} {DATABASE} DataBase {Fore.YELLOW}'{name}'{Fore.RESET} created! {YES}")

def LogDataBaseConnect(name: str) -> None:
    """
    Log a message indicating that a connection to a database has been established.

    Args:
        name (str): The name of the connected database.

    Returns:
        None
    """
    print(f"{LOG} {DATABASE} DataBase {Fore.YELLOW}'{name}'{Fore.RESET} connected! {YES}")

def LogDataBaseNotConnected(name: str) -> None:
    """
    Log a message indicating that a connection to a database could not be established and exit the program.

    Args:
        name (str): The name of the database that failed to connect.

    Returns:
        None
    """
    print(f"{LOG} {DATABASE} DataBase {Fore.YELLOW}'{name}'{Fore.RESET} not connected! {NO}")
    exit(-1)

def LogRecuestRecved(recuest: str) -> None:
    """
    Log a message indicating that a request has been received.

    Args:
        recuest (str): The received request.

    Returns:
        None
    """
    print(f"{LOG} {SERVER} Recuest recved: {Fore.MAGENTA}{recuest}{Fore.RESET}")

def LogInformationAdded(information: list) -> None:
    """
    Log a message indicating that information has been added to the database.

    Args:
        information (list): The information that was added.

    Returns:
        None
    """
    print(f"{LOG} {DATABASE} Added information: {Fore.LIGHTBLUE_EX}{information}{Fore.RESET}")

def LogInformationDeleted(name: str, date: str) -> None:
    """
    Log a message indicating that specific information has been deleted from the database.

    Args:
        name (str): The name associated with the deleted information.
        date (str): The date associated with the deleted information.

    Returns:
        None
    """
    print(f"{LOG} {DATABASE} Deleted information: {Fore.LIGHTBLUE_EX}{name} {date}{Fore.RESET}")

def LogAllInformationDeleted() -> None:
    """
    Log a message indicating that all information has been deleted from the database.

    Returns:
        None
    """
    print(f"{LOG} {DATABASE} All information deleted.")

def LogInformationGetedForDate(date: str, user_id: str):
    """
    Log a message indicating that information has been retrieved for a specific date and user.

    Args:
        date (str): The date for which information was retrieved.
        user_id (str): The ID of the user who requested the information.

    Returns:
        None
    """
    print(f"{LOG} {DATABASE} Information geted for date: {Fore.LIGHTBLUE_EX}{date}{Fore.RESET} by user: {Fore.GREEN}{user_id}{Fore.RESET}")