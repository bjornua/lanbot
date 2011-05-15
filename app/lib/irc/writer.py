# -*- coding: utf-8 -*-
from app.lib.event import Events
from app.lib.ratelimit import TokenBucket
import threading

class Writer(object):
    def __init__(self):
        self.lock = threading.RLock() # (use "with"-block to lock writer)
        self.event = Events()
        self.messagetokens = TokenBucket(5 ,16) # 5 Messages per 16 seconds
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

    def msgline(self, recipient, msg, blocking=True):
        return self.msglines(recipient, [msg], blocking)
    
    def msglines(self, recipient, lines, blocking=True):
        if self.messagetokens.consume(len(lines), blocking):
            for line in lines:
                line = line.encode("utf-8")
                self.command("PRIVMSG", [recipient, line])
            return True
        return False
