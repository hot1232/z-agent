#!/usr/bin/env python
#-*- coding:utf8 -*-

from gevent.queue import Queue
from . import logging

class Chanels(object):
    def __new__(cls, *args, **kw):  
        if not hasattr(cls, '_instance'):  
            orig = super(Chanels, cls)  
            cls._instance = orig.__new__(cls, *args, **kw)
        return cls._instance
    def __init__(self):
        self.logger=logging.getLogger(__name__)
        if not hasattr(self,"_queue_list"):
            self.logger.debug("had no queue_list,init it")
            self._queue_list={}
        self.logger.debug("init chanel, id:%s"%id(self))

    def append(self,queuename):
        #setattr(self, queuename, Queue())
        self.logger.debug("append queue: %s",queuename)
        if not self._queue_list.has_key(queuename):
            self._queue_list[queuename]=Queue(4096)
            self.logger.debug("add queue: %s",queuename)
        return True
    
    def __getitem__(self,key):
        self.logger.debug("queue list : %s, id is: %s",self._queue_list,id(self))
        return self._queue_list.get(key,None)
    
    def __contains__(self,key):
        self.logger.debug("queue list : %s, id is: %s",self._queue_list,id(self))
        if key in self._queue_list.keys():
            return True
        else:
            return False