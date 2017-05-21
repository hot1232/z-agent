#!/usr/bin/env python2.7
# -*- coding:utf8 -*-

import gevent
import time
import gc

import os
libpath=os.path.dirname(__file__).rstrip(__name__)
if not libpath in os.sys.path:
    os.sys.path.append(libpath)

from abc import abstractmethod

from lib.link import Chanels
from lib.log import logging
from lib.decorator import time_me

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
            self.logger.debug("set new checker interval: %s"%self.interval)
        else:
            self.interval=60
        if kwargs.get("timeout",None):
            t = kwargs.pop("timeout")
            self.logger.info("set timeout to %s s"%t)
            self.timeout=gevent.Timeout(t)
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
            t1 = int(time.time())
            try:
                self.timeout.cancel()
                self.timeout.start()
                for ck in self:
                    tgt=getattr(self,"do_check_%s"%ck)
                    if callable(tgt):
                        chan["checker_result_queue"].put({"key":"%s%s"%(ck,self.suffix),"value":tgt(),"clock":t1})
                    else:
                        chan["checker_result_queue"].put({"key":"%s%s"%(ck,self.suffix),"value":tgt,"clock":t1})
                self.timeout.cancel()
            except SystemExit,e:
                self.logger.info("recv exit signal,exiting.")
                raise e
            except AttributeError,e:
                self.logger.error(e)
            except gevent.Timeout:
                self.logger.error("checker %s timeout"%self.__module__)
                self.timeout.cancel()
            except Exception,e:
                self.logger.error("found error: %s"%e)
                self.logger.exception(e)
            
            gc.collect(0)

            t = time.time() - t1
            if t <= self.interval:
                # 睡眠要扣除任务执行时间
                sleep_time = self.interval - t
                self.logger.debug("%s sleep %d sec",self.__module__,sleep_time)
                gevent.sleep(sleep_time)
            else:
                # 任务执行超过定时间隔，交出控制权
                self.logger.error("task time out")
                gevent.sleep() 

class ZabbixSender(object):
    def __init__(self):
        pass
    
    def send(self):
        pass
