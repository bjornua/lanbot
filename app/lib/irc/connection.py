# -*- coding: utf-8 -*-
from app.lib.event import Events

import socket

class Connection(object):
    def __init__(self):
        self.socket = socket.socket()
        self.event = Events()
        self.event.add("send", self.onsend)

    def connect(self, server, port):
        self.socket.connect((server, port))
    
    def recvloop(self):
        while True:
            data = self.socket.recv(4096)
            
            if data == "":
                self.event.notify("disconnect")
                return
            
            self.event.notify("recv", data)

    def onsend(self, data):
        self.socket.sendall(data)
