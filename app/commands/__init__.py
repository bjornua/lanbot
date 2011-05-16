# -*- coding: utf-8 -*-
commands = {}

from pprint import pprint


import os

selfdir, selffilename = os.path.split(__file__)


modulenames = []
for node in os.listdir(selfdir):
    print node
    path = os.path.join(selfdir, node)

    if selffilename == node:
        continue
    
    if os.path.isfile(path):
        name, ext = os.path.splitext(node)
        modulename = name
    elif os.path.isdir(path):
        modulename = node
    else:
        continue

    modulenames += [modulename]

modules = {}
for name in modulenames:
    module = __import__(name, globals(), locals(), [], 1)
    modules[modulename] = module

print (modules)
exit()
