# -*- coding: utf-8 -*-
import app.lib.command

class Command(app.lib.command.BaseCommand):
    name = "banner"
    def exists(self):
        return self.msg.chan != None
    
    def __call__(self):
        self.msg.replylines((
            " _______   __   __  ___  __    __   __          ___      .__   __.",
            "|       \ |  | |  |/  / |  |  |  | |  |        /   \     |  \ |  |",
            "|  .--.  ||  | |  '  /  |  |  |  | |  |       /  ^  \    |   \|  |",
            "|  |  |  ||  | |    <   |  |  |  | |  |      /  /_\  \   |  . `  |",
            "|  '--'  ||  | |  .  \  |  `--'  | |  `----./  _____  \  |  |\   |",
            "|_______/ |__| |__|\__\  \______/  |_______/__/     \__\ |__| \__|"
        ))


