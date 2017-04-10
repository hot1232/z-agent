#!/usr/bin/env python
# -*- coding:utf8 -*-

import os
libpath=os.path.dirname(__file__).rstrip(__name__)
if not libpath in os.sys.path:
    os.sys.path.append(libpath)
    
from lib.log import logging
from abc import abstractmethod

class ExecutorBase(object):
    def __init__(self,*args,**kwargs):
        self.logger=logging.getLogger(self.__module__)
        self._init(*args,**kwargs)
    
    @abstractmethod
    def _init(self,*args,**kwargs):
        pass
        
    @abstractmethod
    def __call__(self,socket, address):
        pass
        
    @staticmethod
    def serve_forever():
        __doc__ = '''
        多进程时使用
        '''
        server.start()
        server.start_accepting()
        server._stop_event.wait()