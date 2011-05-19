import threading

class Limitless(object):
    def consume(self, n, blocking = True):
        return True
        

class TokenBucket(object):
    def __init__(self, tokens, restoredelay):
        self.restoredelay = restoredelay
        self.max = tokens
        self.tokens = tokens
        self.cv = threading.Condition(threading.Lock())
    
    def restore(self, n):
        with self.cv:
            self.tokens += n
            self.cv.notifyAll()

    def consume(self, n, blocking=True):
        if n > self.max:
            raise ValueError("Too many tokens requested.")
        with self.cv:
            while self.tokens < n:
                if blocking == False:
                    return False
                self.cv.wait()
            self.tokens -= n
            threading.Timer(self.restoredelay, self.restore, (n,)).start()
            return True
