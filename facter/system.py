#!/usr/bin/env python
# -*- coding:utf8 -*-

from . import FacterBase

class Facter(FacterBase):
    def _init(self):
        pass

    def facter_sn(self):
        name = ""
        with open("/sys/class/dmi/id/product_serial", "r") as f:
            name = f.read().strip()
        return name

    def facter_vender(self):
        name = ""
        with open("/sys/class/dmi/id/board_vendor", "r") as f:
            name = f.read().strip()
        return name

    def facter_product_name(self):
        name = ""
        with open("/sys/class/dmi/id/product_name", "r") as f:
            name = f.read().strip()
        return name

    def facter_hard_max_open_files(self):
        v = 1024
        with open("/etc/security/limits.conf", "r") as f:
            for line in f:
                if line.startswith("#") or line == "\n":
                    continue
                tgt, ltype, name, value = line.split()
                if tgt == "*" and ltype == "hard" and name == "nofile":
                    v = int(value)
        return v
    def facter_soft_max_open_files(self):
        v = 1024
        with open("/etc/security/limits.conf", "r") as f:
            for line in f:
                if line.startswith("#") or line == "\n":
                    continue
                tgt, ltype, name, value = line.split()
                if tgt == "*" and ltype == "soft" and name == "nofile":
                    v = int(value)
        return v
    