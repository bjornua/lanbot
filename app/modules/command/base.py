# -*- coding: utf-8 -*-
from app.modules.utils.ratelimit import Limitless

class BaseCommand(object):
    rate_limiter = Limitless()
    usage = "There is no help for this command"

    def __init__(self, msg):
        self.msg = msg
    
    def __call__(self, *args, **kwargs):
        self.msg.reply("Not implemented!")

    def exists(self):
        return True
        return self.msg.chan == None

