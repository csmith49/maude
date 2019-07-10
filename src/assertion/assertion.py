# class wrapper for a model assertion that lets us easily store info about the construction
class ModelAssertion:
    def __init__(self, f, **kwargs):
        self._kwargs = kwargs
        self._f = f
    
    # we must maintain the ability to call f
    def __call__(self, *args, **kwargs):
        return self._f(*args, **kwargs)
    
    # otherwise, we just attempt to have an easy way to get some values
    def __getitem__(self, key):
        try:
            return self._kwargs[key]
        except:
            return None

# custom exception for when an assertion is thrown
class ModelAssertionFailure (Exception):
    def __init__(self, msg = None):
        self.msg = msg
    def __str__(self):
        if self.msg:
            return self.msg
        else:
            return "Model assertion failed"

# utility for raising the above
def falsify(msg):
    raise ModelAssertionFailure(msg)

# maintain all the assertions we've seen so far
ASSERTIONS = []

# registration should be straightforward
def modelAssertion(**kwargs):
    def decorator(f):
        assertion = ModelAssertion(f, **kwargs)
        ASSERTIONS.append(assertion)
        return assertion
    return decorator

def modelAssertions():
    return ASSERTIONS