# -*- coding: utf-8 -*-
from app.modules.utils.event import Events
from app.modules.utils.ratelimit import TokenBucket, Limitless
import threading

class Writer(object):
    def __init__(self):
        self.lock = threading.RLock() # (use "with"-block to lock writer)
        self.event = Events()
        self.messagetokens = TokenBucket(6, 16) # 5 Messages per 16 seconds
        self.event.add("line", self.onwriteline)
    
    def onwriteline(self, line):
        with self.lock:
            self.event.notify("data", line + b"\r\n")
    
    def command(self, command, args):
        if(len(args) != 0):
            args[-1] = b":" + args[-1]
            argstr = b" ".join(args)
        else:
            argstr = b""
        
        command = command.encode("iso-8859-1")
        line = command + b" " + argstr

        self.event.notify("line", line)

    def join(self, chan):
        chan = chan.encode("iso-8859-1")
        self.command("JOIN", [chan])

    def part(self, chan):
        self.command("PART", [chan])

    def quit(self, msg):
        self._quit = True
        self.command("QUIT", [msg])
    
    def nick(self, nick):
        nick = nick.encode("iso-8859-1")
        self.command("NICK", [nick])
    
    def user(self, username, hostname, servername, realname):
        username = username.encode("iso-8859-1")
        hostname = hostname.encode("iso-8859-1")
        servername = servername.encode("iso-8859-1")
        realname = realname.encode("utf-8")
        self.command("USER", [username, hostname, servername, realname])
    
    def pong(self, msg):
        self.command("PONG", [msg])

    def msgline(self, recipient, msg, blocking=True):
        return self.msglines(recipient, [msg], blocking)
    
    def msglines(self, recipient, lines, blocking=True):
        recipient = recipient.encode("iso-8859-1")
        if self.messagetokens.consume(len(lines), blocking):
            for line in lines:
                line = line.encode("utf-8")
                self.command("PRIVMSG", [recipient, line])
            return True
        return False
