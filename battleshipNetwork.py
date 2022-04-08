import socket
import pickle
from requests import get


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = socket.gethostbyname_ex(socket.gethostname())[-1]
        for i in self.server:
            if i[0]+i[1]+i[2] == '127':     # Checks to see whether IP is a loopback address
                continue
            else:
                self.server = i
                break
        #print(socket.gethostbyname_ex(socket.gethostname()))
        # socket.gethostname()
        print(self.server)
        self.port = 5555
        self.addr = (self.server, self.port)
        self.client.connect(self.addr)


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
            self.client.send(str.encode(data))
            return pickle.loads(self.client.recv(2048))
        except socket.error as e:
            print(e)
