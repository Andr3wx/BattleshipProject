import socket
import pickle
from requests import get
import os


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.server = socket.gethostbyname_ex(socket.gethostname())[-1]
        #self.server = '172.22.5.117'
        for i in self.server:
            if i[0]+i[1]+i[2] == '127':     # Checks to see whether IP is a loopback address
                continue
            elif i[0] + i[1] != '10':
                continue
            else:
                self.server = i
                break
        print(socket.gethostbyname_ex(socket.gethostname()))
        print(self.server)
        self.port = 5555
        self.addr = (self.server, self.port)
        self.client.connect(self.addr)
        self.p = self.client.recv(2048).decode()
        print(self.p)

    def getP(self):
        return self.p

    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(2048).decode()
        except:
            pass

    def send(self, data):
        try:
            self.client.send(data.encode())
            #return self.client.recv(2048).decode()
        except socket.error as e:
            print(e)

    def receive(self):
        try:
            msg = self.client.recv(2048).decode()
            return msg
        except socket.error as e:
            print(e)
