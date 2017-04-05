import traceback
import gevent
from gevent import monkey
monkey.patch_socket()

import os
libpath=os.path.dirname(__file__).rstrip(__name__)
if not libpath in os.sys.path:
    os.sys.path.append(libpath)

from lib.link import Chanels
from lib.log import logging


class ResultsSender(gevent.Greenlet):
    def __init__(self,*args,**kwargs):
        super(ResultsSender,self).__init__(*args,**kwargs)
        self.logger=logging.getLogger(__name__)
        
    def _run(self,*args,**kwargs):
        chan = Chanels()
        if not "checker_result_queue" in chan:
            chan.append("checker_result_queue")
        self.cls_sender=self.kwargs.get("sender")
        self.kwargs.pop("sender")
        sender=self.cls_sender(*(),**self.kwargs)
        chan=Chanels()
        while True:
            data={}
            try:
                count=0
                while not chan["checker_result_queue"].empty():
                    if count == 20:
                        break
                    sender.add(chan["checker_result_queue"].get())
                    count+=1
                timeout=gevent.Timeout(3)
                timeout.start()
                if sender.data.items_list:
                    sender.send()
                timeout.cancel()
                gevent.sleep(60)
            except gevent.Timeout,e:
                print("timeout: %s"%e)
                continue