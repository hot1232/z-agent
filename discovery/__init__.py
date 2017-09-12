#!/usr/bin/env python2.7
# -*- coding:utf8 -*-

import time
import traceback
import gevent

import os
LIBPATH = os.path.dirname(__file__).rstrip(__name__)
if not LIBPATH in os.sys.path:
    os.sys.path.append(LIBPATH)

from abc import abstractmethod

from lib.link import Chanels
from lib.log import logging
import yaml

class DiscoveryBase(object):
    def __new__(cls, *args, **kw):
        if not hasattr(cls, '_instance'):
            orig = super(DiscoveryBase, cls)
            cls._instance = orig.__new__(cls, *args, **kw)
        return cls._instance

    def __init__(self, run=None, timeout=None, *args, **kwargs):
        super(DiscoveryBase, self).__init__(run=run, *args, **kwargs)
        basepath = os.path.dirname(__file__).rstrip(__name__)
        self.logger = logging.getLogger(self.__module__)
        configfile = ".".join([os.path.join(basepath, "conf", kwargs.get("conf", self.__module__.lstrip("_"))), "yaml"])
        self.logger.debug("concat configfile: %s",configfile)
        if not os.path.exists(configfile):
            configfile = os.path.join(basepath, "conf", "discovery.default.yaml")
        self.config = yaml.load(open(configfile, "r"))
        self.interval = self.config.get("interval", 60)
        self.logger.info("Discoverier: %s 's , use config file: %s , interval is: %s", __name__, configfile, self.interval)
        if not timeout is None:
            self.timeout = gevent.Timeout(timeout)
        else:
            self.timeout = gevent.Timeout(3)
        self.chanel = Chanels()
        if not self.chanel["discovery"]:
            self.logger.debug("add queue: discovery")
            self.chanel.append("discovery")
        if not self.chanel["discovery-sender"]:
            self.logger.debug("add queue: discovery-sender")
            self.chanel.append("discovery-sender")
        self.data = None
        self._init(*args, **kwargs)
    @abstractmethod
    def _init(self, *args, **kwargs):
        pass

    @abstractmethod
    def run(self, **kwargs):
        pass

    def notify_agent_add_check(self):
        if not "discovery" in self.chanel:
            self.chanel.append("discovery")
        self.logger.debug("notify agent to add checker: %s : %s", __name__, self.data)
        self.chanel["discovery"].put({"key":self.__module__.split(".")[-1], "data":self.data["data"]})

    def build_discovery_data(self):
        pass
    
