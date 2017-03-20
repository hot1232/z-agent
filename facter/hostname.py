#!/usr/bin/env python
# -*- coding:utf8 -*-
import os
from . import FacterBase

class Facter(FacterBase):
    def facter_hostname(self):
        return os.uname()[1]

if __name__ == "__main__":
    print os.uname()[1]