# -*- coding: utf-8 -*-
import app.lib.command

class Command(app.lib.command.BaseCommand):
    name = "msg"
    
    def __call__(self, reciever, msg):
        "<nick>|#<channel> <msg>"
        self.bot.client.writer.msgline(reciever, msg)


