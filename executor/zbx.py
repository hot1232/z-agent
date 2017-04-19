#!/usr/bin/env python
# -*- coding:utf8 -*-
from . import ExecutorCoR
from facter.hostname import Facter

class Executor(ExecutorCoR):
    def handle(self, request_str):
        if request_str == "system.hostname":
            self.logger.debug("handle request: system.hostname")
            return Facter()["hostname"]       
        else:
            return super(Executor,self).handle(request_str)
