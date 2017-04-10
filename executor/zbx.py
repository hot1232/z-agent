#!/usr/bin/env python
# -*- coding:utf8 -*-
from . import ExecutorBase
from socket import error as socket_error
from sender import RawSender

class Executor(ExecutorBase):
    def __call__(self,socket, address):
        try:
            socket.settimeout(30)
            while not socket.closed:
                #需要添加身份认证
                data=socket.recv(1024)
                if len(data)==0:
                    continue
                import sender.discovery
                self.logger.debug("recv data:%s"%data)
                send=RawSender(socket=socket,data="t2.dns.koudai.com")
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