# -*- coding: utf-8 -*-
from event import Events

import re
import socket
import threading

re_prefix = "([^!@ ]+)|(([^!]*)!([^@]*)@([^ ]*))"
re_command = "([A-Za-z]+)|([0-9]{3})"
re_params = "(( [^: ][^ ]*)*)( :(.*))?"
re_message = "(:(%s) )?(%s)(%s)?" % (re_prefix, re_command, re_params)
message_matcher = re.compile(re_message)

class Parser(object):
    def __init__(self):
        self.buf = ""

        self.event = Events()

        self.event.add("data", self.ondata)
        self.event.add("line", self.onrecvline)
        self.event.add("msg", self.onmsg)
    
    def reset(self):
        self.buf = ""

    def ondata(self, data):
        self.buf += data
        lines = self.buf.split("\r\n")
        self.buf = lines.pop()
        for line in lines:
            self.event.notify("line", line)

    def onrecvline(self, line):
        match = message_matcher.match(line)
        
        if match == None:
            return
        
        servername = match.group(3)
        nick = match.group(5)
        user = match.group(6)
        host = match.group(7)
        command = match.group(8)
        params = match.group(12).split(" ")[1:]
        trailparam = match.group(15)
        
        if trailparam != None:
            params += [trailparam]
        
        self.event.notify("msg", servername, nick, user, host, command, params)

    def onmsg(self, servername, nick, user, host, command, args):
        if(command == "332"):
            self.event.notify("topic", nick, user, host, args[0], args[1], args[2])
        elif(command == "PING"):
            self.event.notify("ping", args[0])
        elif(command == "NICK"):
            self.event.notify("nick", nick, user, host, args[0])
        elif(command == "NOTICE"):
            self.event.notify("notice", nick, user, host, args[0], args[1])
        elif(command == "PRIVMSG"):
            self.event.notify("privmsg", nick, user, host, args[0], args[1])
        elif(command == "376"):
            self.event.notify("endofmotd", nick, user, host, args[0])
    
class Writer(object):
    def __init__(self):
        self.lock = threading.RLock() # (use "with"-block to lock writer)

        self.event = Events()

        self.event.add("line", self.onwriteline)
    
    def onwriteline(self, line):
        with self.lock:
            self.event.notify("data", line + "\r\n")
    
    def command(self, command, args):
        if(len(args) != 0):
            args[-1] = ":" + args[-1]
            argstr = " ".join(args)
        else:
            argstr = ""

        self.event.notify("line", "%s %s" % (command, argstr))

    def join(self, chan):
        self.command("JOIN", [chan])

    def part(self, chan):
        self.command("PART", [chan])

    def quit(self, msg):
        self._quit = True
        self.command("QUIT", [msg])
    
    def nick(self, nick):
        self.command("NICK", [nick])
    
    def user(self, username, hostname, servername, realname):
        self.command("USER", [username, hostname, servername, realname])
    
    def pong(self, msg):
        self.command("PONG", [msg])

    def msgline(self, recipient, msg):
        self.command("PRIVMSG", [recipient, msg])

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

    def onprivmsg(self, fromnick, fromuser, fromhost, mask, msg):
        if mask.startswith("#"):
            self.event.notify("chanmsg", fromnick, fromuser, fromhost, mask, msg)
        elif mask == self._nick:
            self.event.notify("usermsg", fromnick, fromuser, fromhost, msg)
    
        if self._nick == None:
            self._nick = nick

    def onping(self, token):
        self.writer.pong(token)
    
    def onnick(self, nick, new):
        if nick == self._nick:
            self._nick = new

#while True:
#    client = Client("LANBot")
#    client.writer.event.add("line", lambda line: derp("> " + repr(line)))
#    client.event.add("chanmsg", lambda *args: derp("ChanMSG: " + repr(args)))
#    client.event.add("usermsg", lambda *args: derp("UserMSG: " + repr(args)))
#    client.parser.event.add("line", lambda line: derp("< " + repr(line)))
#    client.parser.event.add("endofmotd", lambda *args: client.writer.join("#dikulan"))
#
#    client.start("irc.freenode.net", 6667)

