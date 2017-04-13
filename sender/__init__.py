import os
import gevent
from gevent import monkey
monkey.patch_socket()

libpath=os.path.dirname(__file__).rstrip(__name__)
if not libpath in os.sys.path:
    os.sys.path.append(libpath)

from lib.link import Chanels
from lib.log import logging

from abc import abstractmethod
import json
import struct
import gc
import yaml



class ResultsSender(gevent.Greenlet):
    def __init__(self,*args,**kwargs):
        super(ResultsSender,self).__init__(*args,**kwargs)
        self.logger=logging.getLogger(self.__module__)
        
    def _run(self,*args,**kwargs):
        self.logger.info("start checker result sender")
        chan = Chanels()
        if not "checker_result_queue" in chan:
            chan.append("checker_result_queue")
        module_name=kwargs.get("klass","zbx")
        module=__import__("sender.%s"%module_name,{},{},[module_name],0)
        self.cls_sender=getattr(module,"Sender")
        self.kwargs.pop("sender")
        chan=Chanels()
        if not "checker_result_queue" in chan:
            chan.append("checker_result_queue")
        while True:
            data={}
            try:
                count=0
                sender=self.cls_sender(*(),**self.kwargs)
                while not chan["checker_result_queue"].empty():
                    if count >=2000:
                        break
                    data=chan["checker_result_queue"].get()
                    self.logger.debug("queue len : %d",chan["checker_result_queue"].qsize())
                    sender.add(**data)
                    count+=1
                timeout=gevent.Timeout(3)
                timeout.start()
                if sender.data.items_list:
                    self.logger.debug("left in queue len : %d",chan["checker_result_queue"].qsize())
                    sender.send()
                del sender
                timeout.cancel()
                gc.collect(0)
            except gevent.Timeout,e:
                self.logger.error("timeout: %s"%e)
            except  Exception,e:
                self.logger.exception(e)
            gevent.sleep(5)

class SenderBase(object):
    #def __new__(cls, *args, **kwargs):       
        #if not hasattr(cls, '_instance'):
            #cls._instance={}
            #orig = super(SenderBase, cls)
            #cls._instance=orig.__new__(cls, *args, **kwargs)
        #return cls._instance
    
    def __init__(self,*args,**kwargs):
        self.logger=logging.getLogger(self.__module__)
        if self.__class__ == SenderBase:
            self.logger.error("class Sender not implemented")
            raise NotImplementedError,"class Sender not implemented"
        basepath=os.path.dirname(__file__).rstrip(__name__)
        configfile=".".join([os.path.join(basepath,"conf",kwargs.get("conf",self.__module__)),"yaml"])
        self.config=yaml.load(open(configfile,"r"))
        self._init(**kwargs)
        
    @abstractmethod
    def _init(self,**kwargs):
        pass
    
    @abstractmethod
    def send(self):
        pass
    
    @abstractmethod
    def add(self,data):
        pass

class RawSender(object):
    def __init__(self,socket=None,data=None):
        self.data=json.dumps(data)
        self.data_len=struct.pack('<Q', len(self.data))
        self.header="ZBXD\1"
        self.socket=socket
        self.logger=logging.getLogger(__name__)
    
    def send(self):
        self.socket.sendall(self.header+self.data_len+self.data)