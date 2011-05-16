# -*- coding: utf-8 -*-

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

print "Found modules: " + ", ".join(modulenames)

modules = {}
onload = []

print "Loading modules"
for name in modulenames:
    print "Loading " + name
    module = __import__(name, globals(), locals(), [], 1)
    modules[modulename] = module

    try:
        onload.append(module.onload)
    except AttributeError:
        pass

for func in onload:
    func()
