#!/usr/bin/env python2.7
# -*- coding:utf8 -*-

from . import ExecutorBase
from . import ExecutorCoR
import zbx
from socket import error as socket_error
from sender import RawSender
from socket import SHUT_RDWR, SOL_SOCKET, SO_LINGER
import agent_executor

class Executor(ExecutorBase):
    def __call__(self,socket, address):
        try:
            socket.settimeout(30)
            while not socket.closed:
                #需要添加身份认证
                data=socket.recv(1024).strip()
                if len(data)==0:
                    self.logger.debug("recv data 0 byte,force close socket")
                    l_onoff = 1                                                                                                                                                           
                    l_linger = 0                                                                                                                                                          
                    socket.setsockopt(SOL_SOCKET, SO_LINGER,                                                                                                                     
                                 struct.pack('ii', l_onoff, l_linger))                    
                    socket.shutdown(SHUT_RDWR)
                    socket.close()
                    break
                self.logger.debug("recv data:%s",data)
                handle=agent_executor.Executor(successor=zbx.Executor(successor=ExecutorCoR()))
                send_data=handle.handle(data)
                self.logger.debug("send data: %s",send_data)
                send=RawSender(socket=socket,data=send_data)
                send.send()
                socket.close()
                #socket.sendall("test")
                #socket.sendall('HTTP/1.1 200 OK\n\npid: %s  data: %s!!\n'%(os.getpid(),data))
            socket.close()
        except socket_error,e:
            (errno,msg)=e
            self.logger.exception("error %s: %s"%(errno,msg))
            if not socket.closed:
                l_onoff = 1                                                                                                                                                           
                l_linger = 0                                                                                                                                                          
                socket.setsockopt(SOL_SOCKET, SO_LINGER,                                                                                                                     
                             struct.pack('ii', l_onoff, l_linger))                    
                socket.shutdown(SHUT_RDWR)              
                socket.close()