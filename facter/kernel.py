#!/usr/bin/env python
# -*- coding:utf8 -*-
from . import FacterBase
import os

class Facter(FacterBase):
    def facter_os_type(self):
        return os.uname()[0]
    def facter_kernel_version(self):
        return os.uname()[2].split("-")[0]
    def facter_kernel_release(self):
        return os.uname()[2]  
    def facter_architecture(self):
        return os.uname()[4]
    

def get():
    return os.uname()[0]

if __name__ == "__main__":
    print os.uname()[0]