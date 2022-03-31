import socket
from _thread import *
import sys
import pickle

server = "172.22.12.73"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


try:
    s.bind((server, port))


except socket.error as e:
    str(e)

s.listen(2)
print("Server started")

connected = set()
games = {}
idCound = 0


def threaded_client(conn, p, gameID):
    global idCount
    conn.send(str.encode(str(p)))

    reply = ""
    while True:
        data = conn.recv(4096).decode()

        if gameId in games:
            game = games[gameId]

            if not data:
                break
            else:

                if data != "get":
                    # if the data being recieved is a move
                reply = game
                conn.sendall(pickle.dumps(reply))


while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    idCount += 1
    p = 0
    gameID = (idCount - 1) // 2
    if idCount % 2 == 1:
        games[gameId] = Game(gameId)
        print("creating a new game")
    else:
        games[gameId].ready = True
        p = 1
    start_new_thread(threaded_client, (conn, p, gameId))
