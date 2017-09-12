#!/usr/bin/env python2.7
# -* coding:utf8 -*-

import time
import functools
from log import logging

logger=logging.getLogger(__name__)

def log_excption(fun):
    """Decorator which translates bare OSError and IOError exceptions
    into NoSuchProcess and AccessDenied.
    """
    @functools.wraps(fun)
    def wrapper(self, *args, **kwargs):
        try:
            return fun(self, *args, **kwargs)
        except Exception as e:
            logger.exception(e)
    return wrapper


def time_me(fn):
    def _wrapper(*args, **kwargs):
        start = time.clock()
        fn(*args, **kwargs)
        logger.debug("%s cost %s second"%(fn.__name__, time.clock() - start))
    return _wrapper

#def time_me(info="used"):
    #def _time_me(fn):
        #@functools.wraps(fn)
        #def _wrapper(*args, **kwargs):
            #start = time.clock()
            #fn(*args, **kwargs)
            #logger.info("%s %s %s seconds",fn.__name__, info, time.clock() - start)
        #return _wrapper
    #return _time_me