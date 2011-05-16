# -*- coding: utf-8 -*-
from app.modules.utils.event import Events

from parser import Parser
from writer import Writer
from connection import Connection

class ChatMessage(object):
    def __init__(self, client, nick, user, host, text, chan=None):
        self.client = client
        self.nick = nick
        self.user = user
        self.host = host
        self.text = text
        self.chan = chan

    def reply(self, text, blocking=True):
        self.replylines([text], blocking)

    def replylines(self, lines, blocking=True):
        self.client.writer.msglines(self.chan or self.nick, lines, blocking)
        

class Client(object):
    def __init__(self, nick):
        self.parser = Parser()
        self.writer = Writer()
        self.conn = Connection()
        
        self.event = Events()

        self.conn.event.add("recv", self.parser.event.notify, "data")
        self.writer.event.add("data", self.conn.event.notify, "send")
        
        self.parser.event.add("nick", self.onnick)
        self.parser.event.add("ping", self.onping)
        self.parser.event.add("privmsg", self.onprivmsg)

        self._nick = nick
        self._quit = False
    
    def start(self, server, port):
        self.conn.connect(server, port)
        self.writer.nick(self._nick)
        self.writer.user("ignored", "ignored", "ignored", "ignored")
        self.conn.recvloop()
    
    def onprivmsg(self, nick, user, host, mask, msg):
        if mask == self._nick:
            mask = None
        elif not mask.startswith("#"):
            return
        
        msg = ChatMessage(self, nick, user, host, msg, mask)
        self.event.notify("chatmsg", msg)

    def onping(self, token):
        self.writer.pong(token)
    
    def onnick(self, nick, user, host, new):
        if nick == self._nick:
            self._nick = new

client = Client("LANBotTest")
parser = client.parser
writer = client.writer
conn = client.conn

def onrecvline(line):
    print "< " + line
parser.event.add("line", onrecvline)

def onsendline(line):
    print "> " + line
writer.event.add("line", onsendline)

def onload():
    client.start("irc.freenode.net", 6667)
