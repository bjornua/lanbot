# -*- coding: utf-8 -*-
import app.lib.irc

class LANBot(object):
    def __init__(self, nick):
        self.client = app.lib.irc.Client(nick)
        self.client.parser.event.listen("chanmsg", self.onchanmsg)
        self.client.parser.event.listen("usermsg", self.onchanmsg)

    def onchanmsg(fromnick, fromuser, fromhost, chan, msg):
        pass
        
    def onusermsg(fromnick, fromuser, fromhost, msg):
        pass
        

#import re
#import app.lib.irc
#import threading
#import collections
#import time
#
#from app.utils import db
#from app.lib.date import nowtuple
#from app.lib.string import parse_command
#from app.model.session import Session
#
#import app.commands.fart
#import app.commands.login
#import app.commands.logout
#import app.commands.join
#import app.commands.msg
#import app.commands.now
#import app.commands.leave
#import app.commands.quit
#import app.commands.blame
#
#
#commands = {}
#for command in (
#    app.commands.fart.Fart,
#    app.commands.login.Login,
#    app.commands.logout.Logout,
#    app.commands.join.Join,
#    app.commands.msg.Msg,
#    app.commands.now.Now,
#    app.commands.leave.Leave,
#    app.commands.quit.Quit,
#    app.commands.blame.Blame,
#):
#    commands[command.name] = command
#
#
#
#
#class LANBot(object):
#    def __init__(self, nick, address, port):
#        self.client = app.lib.irc.Client(nick)
#        self.ratelock = threading.RLock()
#        self.command_last_run = collections.defaultdict(int)
#        
#    def onprivmsg(self, msg, sender_nick, sender_host):
#        msg = unicode(msg, "utf-8", "replace")
#
#        self.onmsg(sender_nick, sender_host, msg)
#
#        db().save({
#            "type": "privmsg",
#            "time": nowtuple(),
#            "sender_nick": sender_nick,
#            "sender_host": sender_host,
#            "msg": msg,
#        })
#            
#    def onchanmsg(self, msg, sender_nick, sender_host, channel):
#        msg = unicode(msg, "utf-8", "replace")
#
#        self.onmsg(sender_nick, sender_host, msg, channel)
#
#        db().save({
#            "type": "chanmsg",
#            "time": nowtuple(),
#            "sender_nick": sender_nick,
#            "sender_host": sender_host,
#            "channel": channel,
#            "msg": msg,
#        })
#
#    def onmsg(self, sender_nick, sender_host, msg, channel = None):
#        m = re.match("!(.+)", msg)
#        if not m == None:
#            try:
#                args = parse_command(m.group(1))
#                command = args[0]
#                args = args[1:]
#            except:
#                raise
#            else:
#                session = Session(sender_nick, sender_host)
#                self.oncommand(session, sender_nick, sender_host, channel, command, args)
#                session.save()
#
#    def oncommand(self, session, sender_nick, sender_host, channel, command, args):
#        command = commands.get(command)
#        
#        now = time.time()
#        
#        with self.ratelock:
#            a = self.command_last_run[command]
#            if now - a - command.rate_limit < 0:
#                return
#            
#            self.command_last_run[command] = now
#        
#        if command == None:
#            return
#        
#        command = command(self, session, sender_nick, sender_host, channel)
#        
#        if not command.exists():
#            return
#
#        if command.require_auth and session.get("user") == None:
#            return
#        
#        try:
#            command.execute(*args)
#        except TypeError:
#            if command.execute.__doc__ == None:
#                command.respond("Usage: !%s" % (command.name,))
#            else:
#                command.respond("Usage: !%s %s" % (command.name, command.execute.__doc__))
#
