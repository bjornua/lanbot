# -*- coding: utf-8 -*-
from app.modules.irc import parser, writer

channels = ()

def onendofmotd(*args):
    for channel in channels:
        writer.join(channel)

parser.event.add("endofmotd", onendofmotd)
