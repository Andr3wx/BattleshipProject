import socket
from _thread import *
import sys
import pickle
from playerClass import Player

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


while True:
    if not twoConnected:
        conn, addr = s.accept()
        print("Connected to:", addr)
        # First connection is player 0 and second connection is player 1
        playersConnected.append(conn)
        conn.send(str(p).encode())
        p += 1
        if p == 2:
            twoConnected = True
    else:
        if playerTurn == 0:
            playersConnected[0].send('Taking Shot'.encode())
            playersConnected[1].send('Placing Ships'.encode())
            print(playersConnected[0].recv(2048).decode())


