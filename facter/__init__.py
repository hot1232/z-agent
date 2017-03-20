#!/usr/bin/env python
# -*- coding:utf8 -*-
import os
libpath=os.path.dirname(__file__).rstrip(__name__)
if not libpath in os.sys.path:
    os.sys.path.append(libpath)

class FacterBase(object):
    def __new__(cls, *args, **kw):       
        if not hasattr(cls, '_instance'):
            cls._instance={}
            orig = super(FacterBase, cls)
            cls._instance=orig.__new__(cls, *args, **kw)
        return cls._instance

    def __getitem__(self,key):
        return getattr(self,"facter_%s"%key)()
    
    def __iter__(self):
        return iter([x.lstrip("facter_") for x in dir(self) if x.startswith("facter_")])