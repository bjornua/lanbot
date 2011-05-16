# -*- coding: utf-8 -*-
from app.modules.utils.event import Events

import re

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
