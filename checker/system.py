#!/usr/bin/env python2.7
# -*- coding:utf8 -*-
#
__author__='liang.zhang'

from . import CheckerBase
import time
import os
import psutil

class Checker(CheckerBase):
    def _init(self):
        self.interval=360
    def do_check_uname(self):
        return ",".join(os.uname())
    def do_check_hostname(self):
        return os.uname()[1]
    def do_check_uptime(self):
        uptime=0
        with open("/proc/uptime","r") as f:
            uptime=float(f.readline().split()[0])
        return uptime
    def do_check_boottime(self):
        btime=""
        with open("/proc/stat","r") as f:
            for line in f:
                ret=line.split()
                if ret[0] == "btime":
                    btime=ret[1]
        if btime:
            return time.strftime("%Y-%m-%d %H:%M:%s",time.localtime(float(btime)))
        else:
            return "0-0-0 00:00:00"
    def do_check_localtime(self):
        return int(time.time())
    
    def do_check_process_count(self):
        return len(psutil.pids())
    
    def do_check_total_logined_users(self):
        return len(psutil.users())
    
    def do_check_open_files_count(self):
        count=0
        for pid in psutil.pids():
            try:
                count+=len(os.listdir("/proc/%s"%pid))
            except:
                continue
        return count
    
    def do_check_zombie_process_count(self):
        count=0
        for pid in psutil.pids():
            try:
                if psutil.Process(pid).status == psutil.STATUS_ZOMBIE:
                    count+=1
            except psutil.NoSuchProcess:
                continue
        return count
    
    def do_check_running_process_count(self):
        count=0
        for pid in psutil.pids():
            try:
                if psutil.Process(pid).status == psutil.STATUS_RUNNING:
                    count+=1
            except psutil.NoSuchProcess:
                continue
        return count
    
    def do_check_waiting_process_count(self):
        count=0
        for pid in psutil.pids():
            try:
                if psutil.Process(pid).status == psutil.STATUS_WAITING:
                    count+=1
            except psutil.NoSuchProcess:
                pass
        return count
    
    def do_check_max_pids(self):
        pid_count = 0
        with open("/proc/sys/kernel/pid_max") as f:
            pid_count=int(f.read())
        return pid_count
    
    def do_check_socket_used(self):
        socket_count = 0
        with open("/proc/net/sockstat","r") as f:
            socket_count = f.readline().split()[2]
        return socket_count
    
    def do_check_tcp_conn(self):
        tcp_conn = 0
        with open("/proc/net/sockstat","r") as f:
            _ = f.readline()
            tcp_conn = f.readline().split()[8]
        return tcp_conn
    
    def do_check_tcp_wait_destroy(self):
        count = 0
        with open("/proc/net/sockstat","r") as f:
            _ = f.readline()
            count = f.readline().split()[4]
        return count
