# -*- coding: utf-8 -*-
import app.lib.command
import datetime

class Now(app.lib.command.Command):
    name = "now"
    
    def exists(self):
        return True
    
    def execute(self):
        tstr = datetime.datetime.now().strftime("%d/%m-%Y kl. %H:%M:%S")
        self.respond(tstr)


