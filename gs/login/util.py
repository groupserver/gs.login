# coding=utf-8
from types import BuiltinFunctionType
try:
    # Python 2.6
    from hashlib import sha1 as sha
    seed_generator = sha
except ImportError:
    # --=mpj17=-- Question: Do we need to support Python 2.4?
    # Python 2.4
    import sha
    seed_generator = sha.sha
assert type(seed_generator) == BuiltinFunctionType,\
    'Did not create the seed generator'
import time, random, logging

logger = logging.getLogger()

def seedGenerator( ):
    s = seed_generator(str(time.time())+str(random.random()))
    retval = s.hexdigest()
    assert retval
    return retval

