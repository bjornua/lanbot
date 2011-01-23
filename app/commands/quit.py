# -*- coding: utf-8 -*-
import app.lib.command

class Quit(app.lib.command.Command):
    name = "quit"
    
    def execute(self, message):
        "<message>"
        self.bot.client.quit(message)
        exit()

