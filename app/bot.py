# -*- coding: utf-8 -*-
import app.lib.irc
from datetime import datetime
from app.lib.string import parsecommand



class LANBot(object):
    def __init__(self, nick):
        self.client = app.lib.irc.Client(nick)
        self.client.event.add("chanmsg", self.onchanmsg)
        self.client.event.add("usermsg", self.onusermsg)
        self.client.parser.event.add("endofmotd", self.onendofmotd)
        self.client.parser.event.add("line", self.onrecvline)
        self.client.writer.event.add("line", self.onsendline)
    
    def onrecvline(self, line):
        print "< " + line
    def onsendline(self, line):
        print "> " + line

    def onendofmotd(self, *args):
        print "Joining #dikulan"
        self.client.writer.join("#dikulan")

    def onchanmsg(self, fromnick, fromuser, fromhost, chan, msg):
        msg = unicode(msg, "utf-8", "replace")
        date = datetime.now().strftime("%H:%M:%S")
        print u"%s - [%s][%s] %s" % (date, chan, fromnick, msg)
        
        if msg.startswith("!"):
            parsed = parsecommand(msg[1:])
            self.client.writer.msgline(chan, repr(parsed), blocking=False)
            self.client.writer.msgline(chan, repr(parsed), blocking=False)

        
    def onusermsg(self, fromnick, fromuser, fromhost, msg):
        msg = unicode(msg, "utf-8", "replace")
        if fromnick == "freeload" and msg == u"!quit":
            self.client.writer.quit("Quitting")
        date = datetime.now().strftime("%H:%M:%S")
        print u"%s - [%s] %s" % (date, fromnick, msg)

