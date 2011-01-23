# -*- coding: utf-8 -*-
import app.lib.command

class Leave(app.lib.command.Command):
    name = "leave"
    def execute(self, channel):
        "<channel>"
        self.bot.client.part(channel)
    

