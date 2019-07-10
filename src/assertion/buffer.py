from collections import deque

# buffer is just a fifo queue that helps us write clean(-ish) code
class Buffer:
    def __init__(self, maxSize=None):
        self._buf = deque([], maxlen=maxSize)
    
    # interface is simple - just push things to the buffer
    def push(self, obj):
        self._buf.append(obj)

    # and get the buffer as a list (possibly of a smaller size)
    def get(self, size=None):
        if size:
            return list(self._buf)[-size:]
        else:
            return list(self._buf)