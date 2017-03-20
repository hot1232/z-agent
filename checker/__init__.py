#!/usr/bin/env python
# -*- coding:utf8 -*-

import gevent
import time
import traceback

import os
libpath=os.path.dirname(__file__).rstrip(__name__)
if not libpath in os.sys.path:
    os.sys.path.append(libpath)

from lib.link import Chanels

class CheckerException(Exception):
    def __init__(self,msg):
        super(CheckerException,self).__init__()
        self.message=msg

class CheckerBase(gevent.Greenlet):
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
            
    def __init__(self,interval=None,run=None,timeout=None,_name=None,*args, **kwargs):
        super(CheckerBase,self).__init__(run=run,*args,**kwargs)
        if interval:
            self.interval=interval
        else:
            self.interval=60
        if not timeout is None:
            self.timeout=gevent.Timeout(timeout)
        else:
            self.timeout=gevent.Timeout(3)
    
    def __iter__(self):
        return iter([x.replace("do_check_","") for x in dir(self) if x.startswith("do_check_")])
    
    def _run(self):
        chan=Chanels()
        result={}
        while True:
            t1 = time.time()
            try:
                self.timeout.cancel()
                self.timeout.start()
                for ck in self:
                    result.update({ck:getattr(self,"do_check_%s"%ck)()})
                self.timeout.cancel()
                if not "checker_result_queue" in chan:
                    chan.append("checker_result_queue")
                print("write data: %s"%result)
                chan["checker_result_queue"].put(result)
            except SystemExit,e:
                raise e
            except AttributeError,e:
                print(e)
                continue
            except gevent.Timeout:
                print("timeout!!")
            except Exception,e:
                traceback.print_exc()
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
