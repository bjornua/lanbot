# -*- coding: utf-8 -*-
import re
import app.lib.irc
import datetime
from app.utils import db
from app.lib.date import nowtuple
from app.lib.string import parse_command

users = set((("freeload", "test1234"),))

class LANBot(object):
    def __init__(self, address, port):
        self.client = app.lib.irc.Client(address, port)
        self.authed_users = set()
        
        prev_onrecvline = self.client.onrecvline
        def onrecvline(line):
            print "> " + line
            prev_onrecvline(line)
        self.client.onrecvline = onrecvline

        prev_sendline = self.client.sendline
        def sendline(line):
            print "< " + line
            prev_sendline(line)
        self.client.sendline = sendline
        
        prev_onusermsg = self.client.onusermsg
        def onusermsg(msg, sender_nick, sender_host):
            self.onprivmsg(msg, sender_nick, sender_host)
            prev_onusermsg(msg, sender_nick, sender_host)
        self.client.onusermsg = onusermsg

        prev_onchanmsg = self.client.onchanmsg
        def onchanmsg(msg, sender_nick, sender_host, channel):
            self.onchanmsg(msg, sender_nick, sender_host, channel)
            prev_onchanmsg(msg, sender_nick, sender_host, channel)
        self.client.onchanmsg = onchanmsg
    
    def onprivmsg(self, msg, sender_nick, sender_host):
        msg = unicode(msg, "utf-8", "replace")
        db().save({
            "type": "privmsg",
            "time": nowtuple(),
            "sender_nick": sender_nick,
            "sender_host": sender_host,
            "msg": msg,
        })
        self.onmsg(sender_nick, sender_host, msg)
            
    def onchanmsg(self, msg, sender_nick, sender_host, channel):
        msg = unicode(msg, "utf-8", "replace")
        db().save({
            "type": "chanmsg",
            "time": nowtuple(),
            "sender_nick": sender_nick,
            "sender_host": sender_host,
            "channel": channel,
            "msg": msg,
        })

        self.onmsg(sender_nick, sender_host, msg, channel)
    
    def onmsg(self, sender_nick, sender_host, msg, channel = None):
        m = re.match("!(.+)", msg)
        if not m == None:
            try:
                args = parse_command(m.group(1))
                command = args[0]
                args = args[1:]
            except:
                raise
            else:
                self.oncommand(sender_nick, sender_host, channel, command, args)
    
    def oncommand(self, sender_nick, sender_host, channel, command, args):
        authed = (sender_nick, sender_host) in self.authed_users

        if not authed and channel == None and command == "login" and len(args) == 2:
            username, password = args
            if (username, password) in users:
                self.authed_users.add((sender_nick, sender_host))
                self.client.msgline(sender_nick, "Authed as %s@%s" % (sender_nick, sender_host))
            else:
                self.client.msgline(sender_nick, "Could not recognize user %s with the given password. Not authed." % (repr(username),))
            return
        
        if authed and command == "logout" and len(args) == 0:
            self.authed_users.discard((sender_nick, sender_host))
            self.client.msgline(sender_nick, "Goodbye, %s." % sender_nick)
            return

        if authed and channel == None and command == "join" and len(args) == 1:
            self.client.join(args[0])
            return
        
        if authed and channel == None and command == "msg" and len(args) == 2:
            self.client.msgline(args[0], args[1])
            return

        if authed and command == "now" and len(args) == 0:
            tstr = datetime.datetime.now().strftime("%d/%m-%Y kl. %H:%M:%S")
            if channel == None:
                self.client.msgline(sender_nick, tstr)
            else:
                self.client.msgline(channel, tstr)
            return

        if authed and command == "fart":
            if channel == None:
                if len(args) == 1:
                    channel = args[0]
                else:
                    return
            for line in (
                " _______   __   __  ___  __    __   __          ___      .__   __.",
                "|       \ |  | |  |/  / |  |  |  | |  |        /   \     |  \ |  |",
                "|  .--.  ||  | |  '  /  |  |  |  | |  |       /  ^  \    |   \|  |",
                "|  |  |  ||  | |    <   |  |  |  | |  |      /  /_\  \   |  . `  |",
                "|  '--'  ||  | |  .  \  |  `--'  | |  `----./  _____  \  |  |\   |",
                "|_______/ |__| |__|\__\  \______/  |_______/__/     \__\ |__| \__|"           
            ):
                self.client.msgline(channel, line)
            return

        if authed and command == "leave" and len(args) == 1:
            self.client.part(args[0])
            return

        if authed and command == "quit" and len(args) == 1:
            self.client.quit(args[0])
            exit()
            return
    
        if authed and channel == None and command == "auth_status" and len(args) == 0:
            self.client.msgline(sender_nick, "Currently authed users:")
            for nick, host in self.authed_users:
                self.client.msgline(sender_nick, "  %s@%s" % (nick, host))
            return

