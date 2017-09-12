from . import DiscoveryBase
#import os
import json
import urllib2
from facter import hostname

class Discovery(DiscoveryBase):
    def _init(self):
        pass
    def run(self):
        try:
            url = "%s?hostname=%s"%(self.config.get("zserver"),hostname.Facter()["hostname"])
            
            req = urllib2.Request(url)
            
            res_data = urllib2.urlopen(req)
            res = res_data.read()
            ret = json.loads(res)
            if ret["status"]!= "00":
                self.data = []
                self.logger.error(ret["message"])
            self.data = " ".join([x for x in ret["data"]])
            self.logger.debug("found application :%s", self.data)
            return self.data
        except Exception as e:
            self.logger.exception(e)
            self.data = None
            return self.data
