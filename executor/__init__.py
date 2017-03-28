#!/usr/bin/env python
# -*- coding:utf8 -*-

import os
libpath=os.path.dirname(__file__).rstrip(__name__)
if not libpath in os.sys.path:
    os.sys.path.append(libpath)
    
from lib.log import logging

class Executor(object):
    def __init__(self):
        self.logger=logging.getLogger(__name__)
        pass
    def __call__(self,socket, address):
        try:
            socket.settimeout(30)
            while not socket.closed:
                #需要添加身份认证
                data=socket.recv(1024)
                if len(data)==0:
                    continue
                import sender.discovery
                print("recv data:%s"%data)
                send=sender.discovery.Sender(socket=socket,data="t2")
                send.send()
                socket.close()
                #socket.sendall("test")
                #socket.sendall('HTTP/1.1 200 OK\n\npid: %s  data: %s!!\n'%(os.getpid(),data))
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