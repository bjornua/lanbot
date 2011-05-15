# -*- coding: utf-8 -*-
from app.lib.ratelimit import Limitless()


class Command(object):
    rate_limiter = Limitless()
    usage = "There is no help for this command"

    def __init__(self, bot, session, msg):
        self.session = session
        self.msg = msg
        self.bot = bot
    
    def run(*args, *kwargs):
        self.msg.respond("Not implemented!")

    def exists(self):
        return self.msg.chan == None

