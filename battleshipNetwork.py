import socket
import pickle
from requests import get


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #ip = get('https://api.ipify.org').content.decode('utf8')
        #print('My public IP address is: {}'.format(ip))

        #print(socket.gethostbyname(socket.getfqdn()))
        #print(self.client.getfqdn())
        self.server = socket.gethostbyname(socket.gethostname())



        # socket.gethostname()
        #print(self.server)
        self.port = 5555
        self.addr = (self.server, self.port)
        self.client.connect(self.addr)
    # def __init__(self):
    #     self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #     self.server = socket.gethostbyname(socket.gethostname())
    #     self.port = 5555
    #     self.addr = (self.server, self.port)
    #     self.p = self.connect()

    # def getP(self):
    #     return self.p
    #
    # def connect(self):
    #     try:
    #         self.client.connect(self.addr)
    #         return self.client.recv(2048).decode()
    #     except:
    #         pass
    #
    # def send(self, data):
    #     try:
    #         self.client.send(str.encode(data))
    #         return pickle.loads(self.client.recv(2048))
    #     except socket.error as e:
    #         print(e)
