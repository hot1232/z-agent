#!/usr/bin/env python
# -*- coding:utf8 -*-
from . import ExecutorCoR
from facter.hostname import Facter

class Executor(ExecutorCoR):
    def handle(self, request_str):
        if request_str == "system.hostname" or request_str == "agent.hostname":
            self.logger.debug("handle request: %s",request_str)
            return Facter()["hostname"]
        elif request_str == "agent.ping":
            self.logger.debug("handle request: agent.ping")
            return 1
        elif request_str == "agent.version":
            self.logger.debug("handle request: agent.version")
            return 2.4        
        else:
            super(Executor,self).handle(request_str)
