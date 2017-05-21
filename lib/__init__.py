#!/usr/bin/env python2.7
# -*- coding:utf8 -*-

import os
libpath=os.path.dirname(__file__).rstrip(__name__)
if not libpath in os.sys.path:
    os.sys.path.append(libpath)
    
from lib.log import logging