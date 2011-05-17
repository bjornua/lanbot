# -*- coding: utf-8 -*-

import os

selfdir, selffilename = os.path.split(__file__)

modulenames = []
for node in os.listdir(selfdir):
    path = os.path.join(selfdir, node)
    if selffilename == node or "__init__.py" == node:
        continue
    
    if os.path.isfile(path):
        name, ext = os.path.splitext(node)
        if ext != ".py":
            continue
        modulename = name
    elif os.path.isdir(path):
        modulename = node
    else:
        continue
    modulenames += [modulename]

print "Found modules: " + ", ".join(modulenames)
modules_ = {}
onload = []

print "Loading modules"
for name in modulenames:
    print "Loading " + name
    module = __import__(name, globals(), locals(), [], 1)
    modules_[modulename] = module

    try:
        onload.append(module.onload)
    except AttributeError:
        pass

for func in onload:
    func()
