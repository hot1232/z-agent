#!/usr/bin/env python
# -*- coding:utf8 -*-

from gevent import monkey
monkey.patch_all()

from lib.log import logging

class Sender(object):
    def __init__(self):
        self.logger=logging.getLogger(__name__)