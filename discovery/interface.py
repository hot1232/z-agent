from . import DiscoveryBase
from facter import interface

class Discovery(DiscoveryBase):
    def _init(self):
        pass
    def run(self):
        interfaces = [{"{#INTERFACENAME}":line} for line in interface.Facter().facter_interfaces ]
        self.data = {"data":interfaces}
        self.logger.debug("found patitions :%s", self.data)
        return self.data
    