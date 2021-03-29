import ac
import sys
import acsys
import socket
import pickle
import os
import time
import platform
import json
import subprocess

if platform.architecture()[0] == "64bit":
    sysdir = os.path.dirname(__file__)+'/stdlib64'
else:
    sysdir = os.path.dirname(__file__)+'/stdlib'

sys.path.insert(0, sysdir)
os.environ['PATH'] = os.environ['PATH'] + ";."

redemption_list = ['', '', '', '', '', '', '', '', '', '']
redemption_label = []
colors = (
    (255, 255, 255), # White
    (0, 255, 128) # Aqua Green
)
color_index = 0
message_offset = 0
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_dir = os.path.dirname(__file__)+'/server.py'
start_server = subprocess.Popen(['cmd', '/k', 'python', '{}'.format(server_dir)])
time.sleep(1.0)

def acMain(ac_version):
    global redemption_list, last_redemption_label, sock
    appWindow = ac.newApp("twitchChannelPoints")
    try:
        sock.connect(('localhost', 443))
        sock.setblocking(False)
        redemption_list.append('Connected to server instance.')
        redemption_list.append('')
    except ConnectionRefusedError as e:
        error = textWrap('Failed to connect to server instance. Make sure to run start_server.bat in assettocorsa/apps/python/twitchChannelPoints before launching the game.')
        for i in error:
            redemption_list.append(i)
        ac.console("TwitchChannelPoints: Failed to connect to server instance. Make sure to run start_server.bat in assettocorsa/apps/python/twitchChannelPoints before launching the game.")
        ac.log("TwitchChannelPoints: Failed to connect to server instance. Make sure to run start_server.bat in assettocorsa/apps/python/twitchChannelPoints before launching the game.")
    ac.setSize(appWindow, 450, 270)
    ac.drawBorder(appWindow,0)
    ac.setBackgroundOpacity(appWindow,0)
    for i in range(0, 10):
        redemption_label.append(ac.addLabel(appWindow, redemption_list[i]))
        ac.setPosition(redemption_label[i], 15, (i * 20) + 40)
        ac.setFontSize(redemption_label[i], 20)
    prevButton = ac.addButton(appWindow, 'ᐃ')
    ac.setSize(prevButton, 20, 20)
    ac.setFontSize(prevButton, 12)
    ac.setPosition(prevButton, 420, 30)
    ac.addOnClickedListener(prevButton, onClickPrev)
    nextButton = ac.addButton(appWindow, 'ᐁ')
    ac.setSize(nextButton, 20, 20)
    ac.setFontSize(nextButton, 12)
    ac.setPosition(nextButton, 420, 210)
    ac.addOnClickedListener(nextButton, onClickNext)
    endButton = ac.addButton(appWindow, 'W')
    ac.setSize(endButton, 20, 20)
    ac.setFontSize(endButton, 12)
    ac.setPosition(endButton, 420, 230)
    ac.addOnClickedListener(endButton, onClickEnd)
    displayRefresh()
    return "appName"


def onClickPrev(v1, v2):
    global message_offset, redemption_list
    if (len(redemption_list) > 10) and (message_offset < (len(redemption_list) - 10)):
        message_offset += 1
        displayRefresh()


def onClickNext(v1, v2):
    global message_offset
    if message_offset > 0:
        message_offset -= 1
        displayRefresh()


def onClickEnd(v1, v2):
    global message_offset
    message_offset = 0
    displayRefresh()


def rangeColor(value):
    OldRange = (255 - 0)
    NewRange = (1 - 0)
    NewValue = (((value - 0) * NewRange) / OldRange) + 0
    return NewValue


def textWrap(data):
    global color_index
    split = []
    length_flag = True
    if isinstance(data, str):
        redemption_list.append(data)
    else:
        username = data['username']
        reward_name = data['reward_name']
        reward_cost = data['reward_cost']
        formatted_message = "{} redeemed '{}' for {} points!".format(username, reward_name, reward_cost)
        rest_message = formatted_message
        while length_flag == True:
            if len(rest_message) > 41:
                split_message = rest_message[:41]
                rest_message = rest_message[41:]
                split.append(split_message)
            else:
                if rest_message.strip() != "":
                    split.append(rest_message)
                length_flag = False
        for i in split:
            redemption_list.append((i, color_index))
        color_index ^= 1
    return


def displayRefresh():
    global redemption_list, redemption_label, message_offset, colors, color_index
    lenList = len(redemption_list)
    for i in range(0, 10):
        current_redemption = redemption_list[i + (lenList - 10) - message_offset]
        if isinstance(current_redemption, tuple):
            message = current_redemption[0]
            message_color_index = current_redemption[1]
            R = rangeColor(colors[message_color_index][0])
            G = rangeColor(colors[message_color_index][1])
            B = rangeColor(colors[message_color_index][2])
            ac.setText(redemption_label[i], "{}".format(message))
            ac.setFontColor(redemption_label[i], R, G, B, 1)
        else:
            ac.setText(redemption_label[i], "{}".format(current_redemption))
        

def acUpdate(deltaT):
    global redemption_list
    try:
        rec_data = sock.recv(8092)
        data = pickle.loads(rec_data)
        if data == []:
            ac.log("TwitchChannelPoints: No new redemptions.")
        else:
            for i in data:      
                textWrap(i)
            displayRefresh()
    except Exception as e:
        pass

def acShutdown():
    global start_server
    pidvalue = start_server.pid
    subprocess.Popen('taskkill /F /T /PID {}'.format(pidvalue))
    return




