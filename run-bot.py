#!/usr/bin/python2 -B
# -*- coding: utf-8 -*-
import app.bot

while True:
    bot = app.bot.LANBot("LANBot")
    bot.client.start("irc.freenode.net", 6667)
