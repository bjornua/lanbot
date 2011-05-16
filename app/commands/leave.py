# -*- coding: utf-8 -*-
import app.lib.command

class Command(app.lib.command.BaseCommand):
    name = "leave"
    def __call__(self, channel):
        "<channel>"
        self.bot.client.writer.part(channel)
