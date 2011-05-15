# -*- coding: utf-8 -*-
import now

commands = {}

for module in (
    now,
):
    command = now.Command
    commands[command.name] = command
