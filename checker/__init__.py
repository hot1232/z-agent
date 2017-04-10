#!/usr/bin/env python
# -*- coding:utf8 -*-

import gevent
import time
import traceback

import os
libpath=os.path.dirname(__file__).rstrip(__name__)
if not libpath in os.sys.path:
    os.sys.path.append(libpath)

from abc import abstractmethod

from lib.link import Chanels
from lib.log import logging

class CheckerException(Exception):
    def __init__(self,msg):
        super(CheckerException,self).__init__()
        self.message=msg

class CheckerBase(gevent.Greenlet):
    mode="static"
    def __new__(cls, *args, **kw): 
        if kw.get("_name",None):
            key=kw["_name"]
        else:
            key=cls.__module__        
        if not hasattr(cls, '_instance'):
            cls._instance={}
            orig = super(CheckerBase, cls)
            cls._instance[key]=orig.__new__(cls, *args, **kw)
        elif not cls._instance.has_key(key):
            orig = super(CheckerBase, cls)
            cls._instance[key]=orig.__new__(cls, *args, **kw)
        return cls._instance[key]
            
    def __init__(self,*args, **kwargs):
        self.logger=logging.getLogger(self.__module__)
        self.suffix=""
        if self.__class__ == CheckerBase:
            raise NotImplementedError,"can not create object of CheckerBase"
        run=kwargs.pop("run",None)
        super(CheckerBase,self).__init__(run=run,*args,**kwargs)
        self._name=kwargs.get("_name")
        if kwargs.get("interval",None):
            self.interval=kwargs.pop("interval")
            self.logger.debug("get new checker interval: %s"%self.interval)
        else:
            self.interval=60
        if kwargs.get("timeout",None):
            self.timeout=gevent.Timeout(kwargs.pop("timeout"))
        else:
            self.timeout=gevent.Timeout(3)
        self._init(*args,**kwargs)
    
    def __eq__(self, other):
        try:
            return self._name == other._name
        except AttributeError:
            return False
        
    def __ne__(self, other):
        try:
            return self._name != other._name
        except AttributeError:
        #发现两者不可比，返回类型错误
            raise TypeError('this two argument is not comparable!')
    @abstractmethod
    def _init(self,*args,**kwargs):
        pass
    
    def __iter__(self):
        if self.mode == "static":
            ret=iter([x.replace("do_check_","") for x in dir(self) if x.startswith("do_check_")])
        else:
            ret=iter([x.replace("do_check_","") for x in dir(self) if x.startswith("do_check_")])
        return ret
            
    
    def _run(self,**kwargs):
        chan=Chanels()
        if not "checker_result_queue" in chan:
            chan.append("checker_result_queue")        
        result={}
        self._name = kwargs.get("_name",None)
        while True:
            t1 = time.time()
            try:
                self.timeout.cancel()
                self.timeout.start()
                for ck in self:
                    tgt=getattr(self,"do_check_%s"%ck)
                    if callable(tgt):
                        result.update({"%s%s"%(ck,self.suffix):tgt()})
                    else:
                        result.update({"%s%s"%(ck,self.suffix):tgt})
                self.timeout.cancel()
                self.logger.debug("write data: %s"%result)
                chan["checker_result_queue"].put(result)
            except SystemExit,e:
                raise e
            except AttributeError,e:
                self.logger.error(e)
                continue
            except gevent.Timeout:
                self.logger.error("checker %s timeout"%__name__)
            except Exception,e:
                self.logger.exception(e)
                continue
            t2 = time.time()

            t = t2 - t1
            if t <= self.interval:
                # 睡眠要扣除任务执行时间
                gevent.sleep(self.interval - t)
            else:
                # 任务执行超过定时间隔，交出控制权
                gevent.sleep() 

class ZabbixSender(object):
    def __init__(self):
        pass
    
    def send(self):
        pass
