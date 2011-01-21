# -*- coding: utf-8 -*-
import re
import app.lib.irc
import datetime


from app.utils import db
from app.lib.date import nowtuple
from app.lib.string import parse_command
from app.model.session import Session
import app.model.user


class LANBot(object):
    def __init__(self, address, port):
        self.client = app.lib.irc.Client(address, port)
        
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
                session = Session(sender_nick, sender_host)
                self.oncommand(session, sender_nick, sender_host, channel, command, args)
                session.save()
    
    def oncommand(self, session, sender_nick, sender_host, channel, command, args):
        def msgsender(msg):
            self.client.msgline(sender_nick, msg)
        
        def respond(msg):
            if channel != None:
                self.client.msgline(channel, msg)
            else:
                msgsender(msg)
            
        def require_login():
            if session.get("user") == None:
                msgsender("Error: You must be logged in to use this command")
                return False
            return True
        
        if command == "login" and channel == None:
            if len(args) != 2:
                respond("Usage: !login <username> <password>")
                return
            
            if session.get("user") != None:
                respond("Error: Already logged in, please log out first")
                return
            
            username, password = args

            id_ = app.model.user.authenticate(username, password)
            if id_ == None:
                respond("Could not recognize user %s with the given password. Not authed" % (repr(username),))
                return
            
            session["user"] = id_
            
            respond("Authed as %s@%s" % (sender_nick, sender_host))
            return

        
        if command == "logout" and channel == None:
            if len(args) != 0:
                respond("Usage: !logout")
                return
            
            if not require_login():
                return
            session["user"] = None
            respond("Goodbye, %s." % (sender_nick,))
            return

        if command == "join" and channel == None:
            if len(args) != 1:
                respond("Usage: !join #<channel>")
                return
            
            if not require_login():
                return
            
            self.client.join(args[0])
            return
        
        if command == "msg" and channel == None:
            if len(args) != 2:
                respond("Usage: !msg <nick>|<channel> <msg>")
                return
            
            if not require_login():
                return
            
            self.client.msgline(args[0], args[1])
            return

        if command == "now":
            if len(args) != 0:
                respond("Usage: !now")
                return
            
            if not require_login():
                return
            
            tstr = datetime.datetime.now().strftime("%d/%m-%Y kl. %H:%M:%S")

            respond(tstr)
            return

        if command == "fart":
            if channel == None:
                if len(args) != 1:
                    respond("Usage: !fart <nick>|<channel>")
                    return
                
                channel = args[0]
            else:
                if len(args) != 0:
                    respond("Usage: !fart")
                
            if not require_login():
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

        if command == "leave":
            if len(args) != 1:
                respond("Usage: !leave <channel>")
                return
            
            if not require_login():
                return

            self.client.part(args[0])
            return

        if command == "quit":
            if len(args) != 1:
                respond("Usage: !quit <message>")
                return
            
            if not require_login():
                return

            self.client.quit(args[0])
            exit()
            return
