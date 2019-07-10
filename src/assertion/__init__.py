from .buffer import Buffer
from .assertion import modelAssertion, modelAssertions, falsify, ModelAssertionFailure
from logging import getLogger

# print out our assertion warnings using a logger for now
logger = getLogger("assertion")

# we maintain a module-wide buffer
_BUFFER = Buffer(maxSize=100)

# need a way to add things to the buffer
def add(obj):
    _BUFFER.push(obj)

# checking is straightforward - take all assertions and apply them to the buffer
def check():
    for assertion in modelAssertions():
        # if the assertion specifies a window, grab it, otherwise use the entire buffer
        context = _BUFFER.get(size=assertion["window"])
        
        # run the assertion - if it raises an exception, capture it and print it out
        try:
            assertion(context)
        except ModelAssertionFailure as e:
            logger.warning("[ASSERTION] %s", e)
        # if any other exception shows up, we're just going to ignore it
        except:
            pass