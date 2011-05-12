# -*- coding: utf-8 -*-
from collections import defaultdict

class Events(object):
    def __init__(self):
        self.signals = defaultdict(list)
    
    def add(self, signal, callback, *args, **kwargs):
        self.signals[signal].append((callback, args, kwargs))
    
    def notify(self, signal, *notifier_args, **notifier_kwargs):
        for callback, observer_args, observer_kwargs in self.signals[signal]:
            kwargs = dict(notifier_kwargs)
            kwargs.update(observer_kwargs)
            args = observer_args + notifier_args
            callback(*args, **kwargs)
