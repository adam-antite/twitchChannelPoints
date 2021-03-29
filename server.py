import asyncio
import socket
import select
import json
import os
import time
import pickle
import sys
from WebSocketClient import WebSocketClient

PATH_APP = os.path.dirname(__file__)
os.environ['PATH'] = os.environ['PATH'] + ';.'

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('localhost', 443))
sock.listen()


async def assettoSocketHandler(client):
    while True:
        print("Waiting for client...")
        client_connection, client_address = sock.accept()
        try:
            print("Client connected.")
            while True:
                client_connection.sendall(pickle.dumps(client.redemption_events_list, protocol=3))
                client.redemption_events_list.clear()
                await asyncio.sleep(3)
        except:
            print("Client disconnected.")
                
        
if __name__ == '__main__':
    client = WebSocketClient()
    loop = asyncio.get_event_loop()
    connection = loop.run_until_complete(client.connect())
    
    tasks = [
        asyncio.ensure_future(assettoSocketHandler(client)),
        asyncio.ensure_future(client.receiveMessage(connection)),
        asyncio.ensure_future(client.heartbeat(connection))
    ]

    loop.run_until_complete(asyncio.wait(tasks))


