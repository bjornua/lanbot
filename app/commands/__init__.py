# -*- coding: utf-8 -*-
import now
import google

commands = {}

for module in (
    now,
    google,
):
    command = module.Command
    print "Adding command: " + command.name
    commands[command.name] = command
