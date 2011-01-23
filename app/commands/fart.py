# -*- coding: utf-8 -*-
import app.lib.command

class Fart(app.lib.command.Command):
    name = "fart"
    def exists(self):
        return self.channel != None
    
    def execute(self):
        for line in (
            " _______   __   __  ___  __    __   __          ___      .__   __.",
            "|       \ |  | |  |/  / |  |  |  | |  |        /   \     |  \ |  |",
            "|  .--.  ||  | |  '  /  |  |  |  | |  |       /  ^  \    |   \|  |",
            "|  |  |  ||  | |    <   |  |  |  | |  |      /  /_\  \   |  . `  |",
            "|  '--'  ||  | |  .  \  |  `--'  | |  `----./  _____  \  |  |\   |",
            "|_______/ |__| |__|\__\  \______/  |_______/__/     \__\ |__| \__|"
        ):
            self.respond(line)


