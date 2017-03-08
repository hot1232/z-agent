from gevent import monkey
monkey.patch_all()

logger = logging.getLogger("compress_log");
logger.setLevel(logging.DEBUG)
ch = logging.FileHandler("/var/log/z-agent.log")
formatter = logging.Formatter('%(asctime)s - %(name)s - %(process)d - %(levelname)s - %(message)s')  
ch.setFormatter(formatter)
logger.addHandler(ch)