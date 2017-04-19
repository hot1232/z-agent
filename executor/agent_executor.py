#!/usr/bin/env python
# -*- coding:utf8 -*-
from . import ExecutorCoR
from facter.hostname import Facter

import psutil
import os

class Executor(ExecutorCoR):
    def handle(self, request_str):
        #agent=globals()["agent"]
        pid=os.getpid()
        p=psutil.Process(pid)
        #if request_str == "agent.routine_number":
            #count=0
            #count=len(agent.facter_list)+len(agent.checker_list)+len(agent.discoverier_spawn_dict)+1
            #return count
        if request_str == "agent.mem_used":
            self.logger.debug("handle request: agent.mem_used")
            return "%0.3f"%p.memory_percent()
        elif request_str == "agent.cpu_used":
            self.logger.debug("handle request: agent.cpu_used")
            return "%0.3f"%p.cpu_percent()
        elif request_str == "agent.ping":
            self.logger.debug("handle request: agent.ping")
            return 1
        elif request_str == "agent.version":
            self.logger.debug("handle request: agent.version")
            return "z-agent 0.1"
        elif request_str == "agent.hostname":
            self.logger.debug("handle request: %s",request_str)
            return Facter()["hostname"]         
        else:
            return super(Executor,self).handle(request_str)
