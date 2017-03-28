from gevent import monkey
monkey.patch_all()
import logging
import cloghandler
import logging.config


#formatter = logging.Formatter('%(asctime)s - %(name)s - %(process)d - %(levelname)s - %(message)s')  

#logger = logging.getLogger("compress_log");
#logger.setLevel(logging.DEBUG)
#ch = logging.FileHandler("/var/log/z-agent.log")
#ch.setFormatter(formatter)
#logger.addHandler(ch)

#ch1=logging.StreamHandler()
#ch1.setFormatter(formatter)
#console = logging.getLogger(__name__)
#console.setLevel(logging.DEBUG)
#console.addHandler()

import os
import yaml

basepath=os.path.dirname(__file__).rstrip(__name__)
yaml_cfg=os.path.join(basepath,"conf","log.yaml")
yaml.load(open(yaml_cfg,"r"))
logging.config.dictConfig(yaml.load(open(yaml_cfg,"r")))