#!/usr/bin/env python2.7
# -*- coding:utf8 -*-

from gevent.server import StreamServer
#from socket import error as socket_error
import imp
import signal
import time
import gc
import os
import sys
#from meliae import scanner

from gevent import monkey
monkey.patch_all()

import gevent

LIBPATH = os.path.dirname(__file__).rstrip(__name__)
if not LIBPATH in os.sys.path:
    os.sys.path.append(LIBPATH)

import checker
import facter
import discovery
import sender.zbx
import sender.discovery
from lib.link import Chanels
from lib.log import logging

from sender import ResultsSender
from executor.base import Executor


class Collector(object):
    def __new__(cls, *args, **kw):
        if not hasattr(cls, '_instance'):
            orig = super(Collector, cls)
            cls._instance = orig.__new__(cls, *args, **kw)
        return cls._instance
    def __init__(self,collecttype="checker"):
        self.logger = logging.getLogger("agent")
        self.mod_list={}
        curdir=os.path.dirname(os.path.realpath(__file__)).rstrip(__name__)
        for cwd,_,files in os.walk(os.path.join(curdir,collecttype)):
            import_prefix=collecttype
            for mod in files:
                if mod.endswith(".py") and mod != "__init__.py":
                    mod_name="%s.%s"%(import_prefix,mod.rstrip(".py"))
                    file, pathname, desc = imp.find_module(mod.rstrip(".py"),[os.path.join(curdir,cwd)])
                    self.logger.debug("load mod: %s",mod_name)
                    self.mod_list[mod.rstrip(".py")]=imp.load_module(mod_name,file,pathname,desc)        
    
    def __iter__(self):
        return iter(self.mod_list.keys())
    def __getitem__(self,key):
        if key in self.mod_list:
            return self.mod_list[key]
        else:
            self.__iter__()
    
        
class ZbxAgent(object):
    def __init__(self):
        pass
    
    def accept_system_uname(self):
        pass
    
    def accept_system_hostname(self):
        pass                

class Agent(object):
    def __new__(cls, *args, **kw):
        if not hasattr(cls, '_instance'):
            orig = super(Agent, cls)
            cls._instance = orig.__new__(cls, *args, **kw)
        return cls._instance    
    def __init__(self,**kwarg):
        self.checker_list={}
        self.server=None
        self.sender=None
        self.facter_list=[]
        self.discoverier_list={}
        self.discoverier_spawn_dict={}
        self.auto_discovery_checker_list=[]
        if __name__ == "__main__":
            name="agent"
        else:
            name=self.__module__
        self.logger=logging.getLogger(name)
        for k,v in kwarg.items():
            setattr(self, k, v)
        self.chanel=Chanels()

    def run_checker(self):
        #start worker thread pool
        #这段代码需要再分析一下

        checker_list=Collector()

        for cker in checker_list:
            self.logger.info("start checker: %s",cker)
            if not hasattr(checker_list[cker],"Checker"):
                self.logger.error("checker: %s not implement",cker)
                continue
            ck=checker_list[cker].Checker()
            if ck.mode == "auto":
                self.logger.info("checker: %s support only auto discover",cker)
                del ck
                continue
            #非单例的使用方式
            #ck2=cc[checker].Checker(_name="test")
            ck.spawn()
            self.checker_list.update({cker:ck})        
    
    def run_facter(self):
        def run_background(interval=1200):
            while True:
                start=int(time.time())
                try:
                    facter_list=Collector(collecttype="facter")
                    for fakter in facter_list:
                        if not hasattr(facter_list[fakter],"Facter"):
                            self.logger.error("facter: %s not implement",fakter)
                            continue
                        fact=facter_list[fakter].Facter()
                        for name in fact:
                            self.logger.info("%s: %s",name,fact[name])
                    gc.collect(0)
                except Exception,e:
                    self.logger.exception(e)
                elapse_time=int(time.time())-start
                gevent.sleep(interval-elapse_time)
        self.logger.info("start facter collective")
        self.facter_list=[gevent.spawn(run_background)]
            
    def run_zbxtrapsender(self):
        self.sender=ResultsSender()
        self.sender.spawn(sender="zbx",mType="items")

    def run_executor(self):
        globals()["agent"]=self
        self.logger.info("start executor")
        self.server = StreamServer(('',10050), Executor(), backlog=100000)
        self.server.start()
        #self.server.init_socket()
        #self.server.start_accepting()
        #self.server._stop_event.wait()
    
    def run_discovery(self):
        def run_background(interval,task_list):
            while True:
                send=sender.discovery.Sender()
                start_t=int(time.time())
                for task in task_list:
                    result=task.run()
                    task.notify_agent_add_check()
                    send.add(task.__module__,result.get("data",[]))
                self.logger.debug("discovery result: %s",result)

                send.send()
                used_t = int(time.time())-start_t
                if interval ==0:
                    interval = 60
                gc.collect(0)
                gevent.sleep(interval-used_t)
        self.logger.info("start discovery")

        all_discoverier_list=Collector(collecttype="discovery")
        discoverier_list = {}

        for discoverier in all_discoverier_list:
            discover = all_discoverier_list[discoverier].Discovery()
            if not discover.interval in discoverier_list:
                discoverier_list[discover.interval]=[]
            if not discover in discoverier_list[discover.interval]:
                discoverier_list[discover.interval].append(discover)

        for discoer_interval in discoverier_list:
            self.logger.debug("run discovery at interval: %s",discoer_interval)
            worker=gevent.spawn(run_background,*(discoer_interval,discoverier_list[discoer_interval]))
            if not discoer_interval in self.discoverier_spawn_dict:
                self.discoverier_spawn_dict.update({discoer_interval:[]})
            if not worker in self.discoverier_spawn_dict[discoer_interval]:
                self.discoverier_spawn_dict[discoer_interval].append(worker)


    def gevent_shutdown(self):
        self.logger.info("kill facter")
        gevent.killall(self.facter_list)
        self.logger.info("kill checker")
        [gevent.killall([self.checker_list[k]]) for k in self.checker_list]
        self.logger.info("kill zbx agent server")
        self.server.close()
        self.logger.info("kill zbx agent trapper")
        gevent.killall([self.sender])
        self.logger.info("kill discover")
        for interval in self.discoverier_spawn_dict:
            gevent.killall(self.discoverier_spawn_dict[interval])
        sys.exit(0)

    def _add_auto_checker(self):
        discover_intervals=[int(k) for k in self.discoverier_spawn_dict]
        if len(discover_intervals) == 0:
            min_discovery_interval = 10
        else:
            min_discovery_interval=min(discover_intervals)
        if not "discovery" in self.chanel:
            self.chanel.append("discovery")
        if not "discovery-sender" in self.chanel:
            self.chanel.append("discovery-sender")        
        while True:
            try:
                while not self.chanel["discovery"].empty():
                    data=self.chanel["discovery"].get()
                    checker_list=Collector()
                    key=data.pop("key")
                    for rcd in data["data"]:
                        key_name="{#%sNAME}"%(key.upper())
                        self.logger.info("add discovery key:%s name: %s",key,rcd[key_name])
                        ck=checker_list[key].Checker(_name=rcd[key_name])
                        if not ck in self.auto_discovery_checker_list:
                            self.logger.info("checker : %s not in auto_discovery_checker_list,start it",ck)
                            ck.spawn(_name=rcd[key_name])
                            self.auto_discovery_checker_list.append(ck)
                        else:
                            self.logger.debug("checker : %s already in auto_discovery_checker_list,pass",ck)
                        del key_name
            except Exception,e:
                self.logger.exception(e)
            gevent.sleep(min_discovery_interval)

    def run_add_auto_checker(self):
        gevent.spawn(self._add_auto_checker)

    def add_static_checker(self):
        pass
    
    @classmethod
    def main(cls):
        agent=cls()
        agent.run_checker()
        agent.run_zbxtrapsender()
        agent.run_facter()
        agent.run_discovery()
        agent.run_executor()
        agent.run_add_auto_checker()
        gevent.signal(signal.SIGQUIT, agent.gevent_shutdown)
        gevent.signal(signal.SIGINT,agent.gevent_shutdown)