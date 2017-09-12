import logging
import re
import simplejson
import socket
import struct
import time

ZBX_HDR = "ZBXD\1"
ZBX_HDR_SIZE = 13

def recv_all(sock):
    buf = ''
    while len(buf)<ZBX_HDR_SIZE:
        chunk = sock.recv(ZBX_HDR_SIZE-len(buf))
        if not chunk:
            return buf
        buf += chunk
    return buf


class AddHostSender(object):

    def __init__(self, zbx_host="", zbx_port=10051):
        self.debug = False
        self.verbosity = False
        self.dryrun = False
        self.request = ""
        self.zbx_host = zbx_host
        self.zbx_port = zbx_port
        self.data_container = ""
        self.logger = logging.getLogger(self.__module__)

    def send_to_zabbix(self, data):
        data_len =  struct.pack('<Q', len(data))
        packet = ZBX_HDR + data_len + data
        zbx_srv_resp_body = ""

        try:
            zbx_sock = socket.socket()
            zbx_sock.connect((self.zbx_host, int(self.zbx_port)))
            zbx_sock.sendall(packet)
        except (socket.gaierror, socket.error) as e:
            zbx_sock.close()
            self.logger.exception(e)
        else:
            try:
                zbx_srv_resp_hdr = recv_all(zbx_sock)
                zbx_srv_resp_body_len = struct.unpack('<Q', zbx_srv_resp_hdr[5:])[0]
                zbx_srv_resp_body = zbx_sock.recv(zbx_srv_resp_body_len)
                zbx_sock.close()
            except:
                zbx_sock.close()

        return simplejson.loads(zbx_srv_resp_body)

    def send(self, hostname,metadata=None):
        data = simplejson.dumps({"host":hostname,"request":"active checks","host_metadata":metadata})
        self.logger.debug(data)
        zbx_answer = self.send_to_zabbix(data)
        self.logger.debug("return: %s"%zbx_answer)
        return zbx_answer
