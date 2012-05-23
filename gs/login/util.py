# coding=utf-8
from hashlib import sha1 as sha
import time, random, logging

logger = logging.getLogger()

def seedGenerator( ):
    s = sha(str(time.time())+str(random.random()))
    retval = s.hexdigest()
    assert retval
    return retval

