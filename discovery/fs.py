from . import DiscoveryBase
import os
import json

class Discovery(DiscoveryBase):
    def run(self):
        with open("/etc/mtab","r") as f:
            partitions=[{"{#FSNAME}":line.split()[1],"{#FSTYPE}":line.split()[2]} for line in f if line.split()[2] in ["xfs","ext4","ext3"]]
        self.data={"data":partitions}
        self.logger.debug("found patitions :%s"%self.data)
        return self.data