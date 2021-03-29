import websockets
import asyncio
import uuid
import requests
import json
import configparser
import os
import ssl
from time import localtime, strftime

PATH_APP = os.path.dirname(__file__)
config_file = os.path.join(PATH_APP, 'config.ini')
config = configparser.ConfigParser()
config.read(config_file)

USER = config['TWITCH']['username']
TOKEN = config['TWITCH']['token']
scope = 'channel:read:redemptions user:read:email'

print("WebSocketClient requirements: ")
print(websockets.version)
print(asyncio.version)
print(uuid.version)
print(requests.version)
print(json.version)
print(configparser.version)
print(os.version)
print(ssl.version)
print(time.version)

class WebSocketClient():
    redemption_events_list = []
        
    def __init__(self):
        # Check if existing token is still valid
        if TOKEN:
            try:
                headers = {
                    'Client-ID': 'e6egls0ukji6rok7lvw7kyhaf77woo',
                    'Authorization': 'OAuth ' + TOKEN
                }
                response = requests.get('https://id.twitch.tv/oauth2/validate', headers=headers)
                print("Token check response: ")
                logging.info("Token check response: ")
                print(response)
                logging.info(response)
            except Exception as e:
                print("Exception in __init__(): " + str(e))

        # Get Channel ID using token
        headers = {
            'Client-ID': 'e6egls0ukji6rok7lvw7kyhaf77woo',
            'Authorization': 'Bearer ' + TOKEN
        }
        response = requests.get('https://api.twitch.tv/helix/users?login=' + USER, headers=headers)
        response = json.loads(response.text)
        config['TWITCH']['channel_id'] = response['data'][0]['id']
        #print("Get channel ID response: ")
        #print(response)
        with open('config.ini', 'w') as configfile:
            config.write(configfile)
        self.topics = ["channel-points-channel-v1." + config['TWITCH']['channel_id']]
        self.auth_token = config['TWITCH']['token']
        pass


    async def connect(self):
        '''
           Connecting to WebSocket server
           websockets.client.connect returns a WebSocketClientProtocol
           which is used to send and receive messages
        '''
        print("Attempting connection to Twitch API...")
        self.connection = await websockets.client.connect('wss://pubsub-edge.twitch.tv/',
                                                           ssl=ssl.SSLContext(ssl.PROTOCOL_TLSv1))
        if self.connection.open:
            message = {"type": "LISTEN",
                       "nonce": str(self.generate_nonce()),
                       "data": {"topics": self.topics,
                                "auth_token": self.auth_token}
                       }
            json_message = json.dumps(message)
            await self.sendMessage(json_message)
            print("Connection established to Twitch API.")
            return self.connection


    def generate_nonce(self):
        '''Generate pseudo-random number and seconds since epoch (UTC).'''
        nonce = uuid.uuid1()
        oauth_nonce = nonce.hex
        return oauth_nonce


    async def sendMessage(self, message):
        '''Sending message to Twitch API WebSocket server'''
        try:
            message_json = json.loads(message)
            await self.connection.send(message)
        except Exception as e:
            print('Error in sendMessage(): ' + str(e))


    async def receiveMessage(self, connection):
        '''Receiving all server messages and handling them'''
        while True:
            try:
                message = await connection.recv()
                message_json = json.loads(message)
                if message_json['type'] != 'PONG':
                    print(message_json)
                if message_json['type'] == 'MESSAGE':
                    raw_redemption_message = message_json['data']['message']
                    redemption_message_json = json.loads(raw_redemption_message)
                    username = redemption_message_json['data']['redemption']['user']['display_name']
                    reward_name = redemption_message_json['data']['redemption']['reward']['title']
                    reward_cost = redemption_message_json['data']['redemption']['reward']['cost']
                    new_redemption_event = {"username": username, "reward_name": reward_name, "reward_cost": reward_cost}
                    self.redemption_events_list.append(new_redemption_event)
                    print(new_redemption_event)
                elif message_json['type'] == 'PONG':
                    print(strftime("%H:%M:%S", localtime()) + " - " + "Received PONG from server.")
                elif message_json['type'] == 'RECONNECT':
                    print("Server sent RECONNECT message.")
            except websockets.exceptions.ConnectionClosed:
                print('Error in receiveMessage(): Connection with Twitch API closed.')
                self.redemption_events_list.append('Server connection to Twitch API closed.')
                break


    async def heartbeat(self, connection):
        '''Keeps connection with server alive with pings every 4 minutes'''
        while True:
            try:
                data_set = {"type": "PING"}
                json_request = json.dumps(data_set)
                await connection.send(json_request)
                print(strftime("%H:%M:%S", localtime()) + " - " + "PING sent to server.")
                await asyncio.sleep(180)
            except websockets.exceptions.ConnectionClosed:
                print('Error in heartbeat(): Connection with Twitch API closed.')
                break

