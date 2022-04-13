import socket
from _thread import *
import sys
import pickle
from playerClass import Player
import time
import threading

# Create worker threads
# def create_workers():
completeSetup = ['', '']
whichTurn = 0
intendedMsg = ''


def handle_client(connection, player):
    global completeSetup
    global whichTurn
    global intendedMsg
    # Sends player their player number
    connection.send(str(p).encode())
    # At the beginning of the game, sets both players to placing ships
    connection.send('Placing Ships'.encode())

    completeSetup[player] = connection.recv(2048).decode()
    while completeSetup[0] == '' or completeSetup[1] == '':
        continue
    print('done')
    if player == 0:
        connection.send('Taking Shot'.encode())
    else:
        connection.send('Taking Shot'.encode())

    # while True:
    #     # if its this threads players turn
    #     if whichTurn == player:
    #         # Waits to see what move the player is going to take
    #         data = conn.recv(2048).decode()
    #         # Gives value to global variable allowing other thread to see
    #         intendedMsg = data
    #         time.sleep(1)   # Gives other thread chance to see message first
    #     else:
    #         if intendedMsg != '':
    #             # Sends message from other thread to app
    #             connection.send(intendedMsg).encode()
    #             # Resets the message so that other thread waits for move
    #             intendedMsg = ''
    #             # Switches player turn
    #             if whichTurn == 0:
    #                 whichTurn = 1
    #             else:
    #                 whichTurn = 0




server = ''
port = 5555
global idCount

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server = socket.gethostbyname_ex(socket.gethostname())[-1]

for i in server:
    if i[0] + i[1] + i[2] == '127':  # Checks to see whether IP is a loopback address
        continue
    else:
        server = i
        break
print(server)
try:
    s.bind((server, port))

    print("yes")
except socket.error as e:
    str(e)

s.listen(2)
print("Server started")

p = 0
twoConnected = False
playerTurn = 0
playersConnected = []
playerAddress = []
iniSetup = True
threads = []

while True:
    if len(playersConnected) < 2:
        conn, addr = s.accept()
        print("Connected to:", addr)
        # First connection is player 0 and second connection is player 1
        playersConnected.append(conn)
        playerAddress.append(addr)
        t = threading.Thread(target=handle_client,args=(conn,p),daemon=True)
        t.start()
        p += 1
    # else:
    #     print(playersConnected)
    #     for connect in range(1,len(playersConnected)):
    #         print('in')
    #         threads.append(threading.Thread(target=handle_client,args=(playersConnected[connect],connect),daemon=True))
    #         threads[connect].start()


