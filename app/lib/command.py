# -*- coding: utf-8 -*-
class Command(object):
    require_auth = True
    rate_limit = 0
    def __init__(self, bot, session, sender_nick, sender_host, channel):
        self.session = session
        self.sender_nick = sender_nick
        self.sender_host = sender_host
        self.channel = channel
        self.bot = bot
    
    def respond(self, msg):
        if self.channel != None:
            self.bot.client.msgline(self.channel, msg)
        else:
            self.bot.client.msgline(self.sender_nick, msg)
    
    def exists(self):
        return self.channel == None

