# -*- coding: utf-8 -*-
import app.lib.irc
from datetime import datetime

class LANBot(object):
    def __init__(self, nick):
        self.client = app.lib.irc.Client(nick)
        self.client.event.add("chanmsg", self.onchanmsg)
        self.client.event.add("usermsg", self.onusermsg)
        self.client.parser.event.add("endofmotd", self.onendofmotd)

    def onendofmotd(self, *args):
        self.client.writer.join("#dikulan")

    def onchanmsg(self, fromnick, fromuser, fromhost, chan, msg):
        msg = unicode(msg, "utf-8", "replace")
        date = datetime.now().strftime("%H:%M:%S")
        print "%s - [%s][%s] %s" % (date, chan, fromnick, msg)
        
    def onusermsg(self, fromnick, fromuser, fromhost, msg):
        msg = unicode(msg, "utf-8", "replace")
        if fromnick == "freeload" and msg == u"!quit":
            self.client.writer.quit("Quitting")
        date = datetime.now().strftime("%H:%M:%S")
        print "%s - [%s] %s" % (date, fromnick, msg)

