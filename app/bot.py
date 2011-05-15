# -*- coding: utf-8 -*-
import app.lib.irc.client
from datetime import datetime
from app.lib.string import parsecommand

from threading import Thread

from app.commands import commands


class LANBot(object):
    def __init__(self, nick):
        self.client = app.lib.irc.client.Client(nick)
        self.client.event.add("chatmsg", self.onchatmsg)
        self.client.parser.event.add("endofmotd", self.onendofmotd)
        self.client.parser.event.add("line", self.onrecvline)
        self.client.writer.event.add("line", self.onsendline)

    
    def onrecvline(self, line):
        print "< " + line
    def onsendline(self, line):
        print "> " + line

    def onendofmotd(self, *args):
        self.client.writer.join("#dikulan")

    def onchatmsg(self, msg):
        msg.text = unicode(msg.text, "utf-8", "replace")
        
        if msg.text.startswith("!"):
            args = parsecommand(msg.text[1:])
            if len(args) != 0:
                Thread(target=self.oncommand, args=(msg,args[0],args[1:])).start()
    
    def oncommand(self, msg, command, args):
        try:
            command = commands[command]
        except KeyError:
            return
        command = command(self, None, msg)
        if not command.exists():
            return
        command(*args)

        
