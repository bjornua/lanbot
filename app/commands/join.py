# -*- coding: utf-8 -*-
import app.lib.command

class Join(app.lib.command.Command):
    name = "join"
    def execute(self, channel):
        "#<channel>"
        self.bot.client.join(channel)


