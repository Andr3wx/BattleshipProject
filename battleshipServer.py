import socket
from _thread import *
import sys
import pickle
from playerClass import Player


server = ''
#
port = 5555
global idCount

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


try:
    s.bind((server, port))
    # print("yes")


except socket.error as e:
    str(e)

s.listen(2)
print("Server started")
while True:
    print("in")
    conn,addr =s.accept()
    print(conn)

connected = set()
games = {}
idCount = 0


# def threaded_client(conn, p, gameID):
#
#     conn.send(str.encode(str(p)))
#
#     reply = ""
#     while True:
#         try:
#
#             data = conn.recv(4096).decode()
#
#             if gameID in games:
#                 game = games[gameID]
#
#                 if not data:
#                     break
#                 else:
#
#                     if data != "get":
#                         # if the data being recieved is a move
#
#                         reply = game
#                         conn.sendall(pickle.dumps(reply))
#                     elif data == "win" or data == "lose":
#                         game.reset()
#             else:
#                 break
#         except:
#             break
#     print("lost connection")
#     print("closing game", gameID)
#     try:
#         del games[gameID]
#     except:
#         pass
#     idCount -= 1
#     conn.close()
#
#
# while True:
#     conn, addr = s.accept()
#     print("Connected to:", addr)
#
#     idCount += 1
#     p = 0
#     gameID = (idCount - 1) // 2
#     if idCount % 2 == 1:
#         games[gameID] = Player(gameID)
#         print("creating a new game")
#     else:
#         games[gameID].ready = True
#         p = 1
#     start_new_thread(threaded_client, (conn, p, gameID))
