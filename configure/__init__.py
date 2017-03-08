#!/usr/bin/env python
# -*- coding:utf8 -*-

from ConfigParser import ConfigParser


class ConfigBase(object):
    
    def __iter__(self):
        return iter([x.lstrip("facter_") for x in dir(self) if x.startswith("facter_")])

