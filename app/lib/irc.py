# -*- coding: utf-8 -*-
import re
import socket
class BasicClient(object):
    def __init__(self):
        self.buf = ""
        self._nick = None
    
    def onrecv(self, data):
        self.buf += data
        lines = self.buf.split("\r\n")
        self.buf = lines.pop()
        for line in lines:
            self.onrecvline(line)
    
    def onrecvline(self, line):
        prefix = "([^!@ ]+)|(([^!]*)!([^@]*)@([^ ]*))"
        command = "([A-Za-z]+)|([0-9]{3})"
        params = "(( [^: ][^ ]*)*)( :(.*))?"
        message = "(:(%s) )?(%s)(%s)?" % (prefix, command, params)
        match = re.match(message, line)
        
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
        
        self.onmsg(servername, nick, user, host, command, params)
        
    def join(self, chan):
        self.command("JOIN", [chan])

    def part(self, chan):
        self.command("PART", [chan])

    def quit(self, msg):
        self.command("QUIT", [msg])
    
    def nick(self, nick):
        self.command("NICK", [nick])
        if self._nick == None:
            self._nick = nick
    
    def user(self, username, hostname, servername, realname):
        self.command("USER", [username, hostname, servername, realname])
    
    def pong(self, msg):
        self.command("PONG", [msg])
    
    def msgline(self, recipient, msg):
        self.command("PRIVMSG", [recipient, msg])
    
    def command(self, command, args):
        if(len(args) != 0):
            args[-1] = ":" + args[-1]
            argstr = " ".join(args)
        else:
            argstr = ""
        
        self.sendline("%s %s" % (command, argstr))
        
    def sendline(self, string):
        self.send(string + "\r\n")

    def send(self, data):
        pass
        
    def onmsg(self, servername, nick, user, host, command, args):
        if(command == "PING"):
            self.onping(args[0])
        if(command == "NICK"):
            self.onnick(nick, args[0])
        if(command == "PRIVMSG"):
            self.onprivmsg(args[1], nick, host, args[0])
    
    def onprivmsg(self, msg, sender_nick, sender_host, recipient):
        if recipient.startswith("#"):
            self.onchanmsg(msg, sender_nick, sender_host, recipient)
        elif recipient == self._nick:
            self.onusermsg(msg, sender_nick, sender_host)
    
    def onchanmsg(self, msg, sender_nick, sender_host, channel):
        pass
    
    def onusermsg(self, msg, sender_nick, sender_host):
        pass
    
    def onping(self, token):
        self.pong(token)
    
    def onnick(self, nick, new):
        if nick == self._nick:
            self._nick = new
        print self._nick
    
class SocketClient(BasicClient):
    def __init__(self, socket):
        BasicClient.__init__(self)
        self.socket = socket
    
    def loop(self):
        while True:
            data = self.socket.recv(4096)
            self.onrecv(data)

    def send(self, data):
        BasicClient.send(self, data)
        self.socket.sendall(data)

class Client(SocketClient):
    def __init__(self, address, port):
        sock = socket.socket()
        sock.connect((address, port))
        SocketClient.__init__(self, sock)
