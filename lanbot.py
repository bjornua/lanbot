#!/usr/bin/python -B
# -*- coding: utf-8 -*-
import random
import socket
import threading
import time
import re
import shlex
import lib.irc
import datetime

users = set((("freeload", "test1234"),))


class LanBOT(lib.irc.Client):
    def __init__(self):
        lib.irc.Client.__init__(self)
        self.authed_users = set()
    
    def onprivmsg(self, msg, sender_nick, sender_host, recipient):
        lib.irc.Client.onprivmsg(self, msg, sender_nick, sender_host, recipient)
        
        authed = (sender_nick, sender_host) in self.authed_users
        
        m = re.match("cmd (.*)", msg)
        if m == None:
            return

        try:
            args = shlex.split(m.group(1))
            command = args[0]
            args = args[1:]
        except:
            return
        
        if command == "login" and len(args) == 2:
            if(recipient.startswith("#")):
                return
            username, password = args
            if (username, password) in users:
                self.authed_users.add((sender_nick, sender_host))
                self.msgline(sender_nick, "Authed as " + sender_nick + "@" + sender_host)
        
        if authed and command == "logout" and len(args) == 0:
            self.authed_users.discard((sender_nick, sender_host))
            self.msgline(sender_nick, "Logged out")
        
        if authed and command == "now":
            tstr = datetime.datetime.now().strftime("%d/%m-%Y kl. %H:%M:%S")
            if recipient.startswith("#"):
                self.msgline(recipient, tstr)
            else:
                self.msgline(sender_nick, tstr)
        
        if authed and command == "join" and len(args) == 1:
            self.join(args[0])

        if authed and command == "leave" and len(args) == 1:
            self.part(args[0])

        if authed and command == "quit" and len(args) == 1:
            self.quit(args[0])
            exit()
        
        if authed and command == "auth_status" and len(args) == 0:
            if(recipient.startswith("#")):
                return
            self.msgline(sender_nick, "Currently authed users:")
            for nick, host in self.authed_users:
                self.msgline(sender_nick, "  %s@%s" % (nick, host))

        if authed and command == "msg" and len(args) == 2:
            if(recipient.startswith("#")):
                return
            self.msgline(sender_nick, "Currently authed users:")
            for nick, host in self.authed_users:
                self.msgline(sender_nick, "  %s@%s" % (nick, host))
    
class ConnectedLanBOT(LanBOT):
    def __init__(self, sock):
        LanBOT.__init__(self)
        self.sock = sock
    
    def loop(self):
        while True:
            data = self.sock.recv(1)
            self.onrecv(data)

    def send(self, data):
        LanBOT.send(self, data)
        self.sock.sendall(data)
        

sock = socket.socket()
sock.connect(("clanserver4u2.de.quakenet.org", 6667))

#sock.connect(("gibson.freenode.net", 6667))

bot = ConnectedLanBOT(sock)


bot.nick("LanBOT")
bot.user("LanBOT", "ignored", "ignored", "Testbot")

bot.loop()

bot = LanBOT()