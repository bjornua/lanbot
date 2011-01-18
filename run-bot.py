#!/usr/bin/python -B
# -*- coding: utf-8 -*-
import app.bot

bot = app.bot.LANBot("irc.freenode.net", 6667)

bot.client.nick("LANBot")
bot.client.user("LANBot", "*", "*", "*")

bot.client.loop()
