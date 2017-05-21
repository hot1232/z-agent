#!/usr/bin/env python2.7
# -*- coding:utf8 -*-

from gevent import monkey
monkey.patch_all()

import os
import time
import click

import gevent
from gevent.threadpool import ThreadPool
from gevent.queue import Queue,Empty
from gevent.event import AsyncResult
from gevent.lock import BoundedSemaphore
from gevent.pool import Pool
from gevent.server import StreamServer
from multiprocessing import Process
from socket import error as socket_error

def main(args):
    pass

def daemon(func,args=None):
    __doc__ = '''
    name: daemon
    description: daemonize main process，暂时没有用到这个函数
    input:
          None
    output:
          None
    '''
    pid=os.fork();
    if pid > 0:
        sys.exit(0);
    elif pid == 0:
        os.chdir("/");
        os.umask(0);
        os.setsid();
        pid2=os.fork();
        if pid2 > 0:
            logger.info("daemon start with pid: {0}".format(pid2))
            open("/var/run/z-agent.pid","w").write("%s"%pid2);
        elif pid2 == 0:
            for f in sys.stdout, sys.stderr: f.flush();
            si = file("/dev/null", 'r');
            so = open("/var/log/agent.log",'a');
            os.dup2(si.fileno(), sys.stdin.fileno())
            os.dup2(so.fileno(), sys.stdout.fileno())
            os.dup2(so.fileno(), sys.stderr.fileno())
            if args:
                func(args);
            else:
                func();
        else:
            print("2 fork failed");
    else:
        print("fork failed!");

class MainProcess(gevent.Greenlet):
    def __init__(self, run=None,*args, **kwargs):
        super(MainProcess,self).__init__(run=run,*args,**kwargs)
    def _run(self):
        gevent.sleep(10)
        print("haha")

#evt=AsyncResult()
evt=Queue()
b = BoundedSemaphore(1)
def t1():
    global evt,b
    while True:
        try:
            with b:
                data=evt.get(timeout=2)
            if data:
                print("1 recv data: %s"%data)
        except Empty:
            gevent.sleep(1)

def t2():
    global evt
    for i in xrange(20000):
        evt.put(i)
        print("put: %d"%i)
    return "over"

def t3():
    global evt,b
    while True:
        try:
            with b:
                data=evt.get(timeout=2)
            if data:
                print("2 recv data: %s"%data)
        except Empty:
            gevent.sleep(1)

def cb(result):
    print(result)
    
class CommandRunner(object):
    def __init__(self):
        pass
    def __call__(self,socket, address):
        try:
            socket.settimeout(30)
            while not socket.closed:
                #需要添加身份认证
                data=socket.recv(1024)
                socket.sendall('HTTP/1.1 200 OK\n\npid: %s count: %s  data: %s!!\n'%(os.getpid(),self.count,data))
            socket.close()
        except socket_error,e:
            (errno,msg)=e
            print("error %s: %s"%(errno,msg))
            if not socket.closed:
                socket.close()
        
    @staticmethod
    def serve_forever():
        __doc__ = '''
        多进程时使用
        '''
        server.start()
        server.start_accepting()
        server._stop_event.wait()
        

if __name__ == "__main__":
    #start worker thread pool
    pool =ThreadPool(4)
    #c=pool.spawn(t2)
    
    #start command runner processes
    #process_count = 4
    #process_list=[]
    #需要添加配置读取代码
    server = StreamServer(('',10052), CommandRunner(), backlog=100000)
    server.init_socket()
    
    server.start()
    server.start_accepting()
    server._stop_event.wait()
    
    #for i in range(process_count - 1):
    #    p=Process(target=CommandRunner.serve_forever, args=tuple())
    #    p.start()
    #    process_list.append(p)
