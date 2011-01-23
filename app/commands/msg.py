# -*- coding: utf-8 -*-
import app.lib.command

class Msg(app.lib.command.Command):
    name = "msg"
    
    def execute(self, reciever, msg):
        "<nick>|#<channel> <msg>"
        self.bot.client.msgline(reciever, msg)


