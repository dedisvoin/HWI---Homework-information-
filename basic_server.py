from src import api
import time

server = api.HWIServer()
server.create_data_base() 
server.clean_data_base() # предварительная очистка бд для теста
server.run()
