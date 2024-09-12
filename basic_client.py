# подключаешь api
from src import api

import time

# создание обьекта клиента для сессии (порт хост)
ClientObject = api.HWIClient()

# подключение к серверу 
ClientObject.connect()

time.sleep(1) # чтобы сервер успел принять подключение

ClientObject.request(api.Requests.ADD_INFO(['Mark', 'история', '16.12.2024', '19.02.2024', 'что-то']))

time.sleep(1)
ClientObject.request(api.Requests.ADD_INFO(['Mark', 'история', '16.11.2024', '19.02.2024', 'что-то']))
time.sleep(1)
print(ClientObject.request(api.Requests.GET_ALL))