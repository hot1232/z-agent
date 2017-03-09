#!/usr/bin/env python
# -*- coding:utf8 -*-
__doc__='''
姣忎釜checker閮藉簲鍖呭惈涓�釜Checker绫�姣忎釜Checker绫婚兘搴旀湁涓�釜interval绫诲彉閲�'''

class CheckerException(Exception):
    def __init__(self,msg):
        super(CheckerException,self).__init__()
        self.message=msg

class CheckerBase(object): 
    interval=300
    def __new__(cls, *args, **kw):  
        if not hasattr(cls, '_instance'):  
            orig = super(CheckerBase, cls)  
            cls._instance = orig.__new__(cls, *args, **kw)  
        return cls._instance

    def __init__(self,interval=None):
        self.interval=interval

    def __getattr__(self,key):
        return getattr(self,"do_%s"%key)()
    
    def __iter__(self):
        return iter([x.lstrip("do_") for x in dir(self) if x.startswith("do_")])
    
    def do_t1(self):
        return 0;

class ZabbixSender(object):
    def __init__(self):
        pass
    
    def send(self):
        pass
#c=T1()
#c.main()
#if hasattr(c,"t1"):
#    print(c.t1)
#for i in c:
#    print(i)