# -*- coding: utf-8 -*-
import app.lib.command
import app.model.search

class Blame(app.lib.command.Command):
    name = "blame"
    require_auth = False
    rate_limit = 5 # Minimum time between request
    
    def exists(self):
        return self.channel != None
    
    def execute(self, word):
        "<word>"
        
        result = app.model.search.search(self.channel, word)
        
        if result == None:
            return
        
        time, sender_nick, msg = result
        
        tstr = time.strftime("%d/%m-%Y %H:%M:%S")
        self.respond("[%s] <%s> %s" % (tstr, sender_nick, msg))
