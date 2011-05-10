# -*- coding: utf-8 -*-
class Event(object):
    def __init__(self):
        self.listeners = []
    
    def listen(self, callback, *args, **kwargs):
        self.listeners.append((callback, args, kwargs))
    
    def notify(self, *notifier_args, **notifier_kwargs):
        for callback, observer_args, observer_kwargs in self.listeners:
            kwargs = dict(notifier_kwargs)
            kwargs.update(observer_kwargs)
            args = observer_args + notifier_args
            callback(*args, **kwargs)
