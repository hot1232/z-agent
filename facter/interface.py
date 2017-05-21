#!/usr/bin/env python2.7
# -*- coding:utf8 -*-

from . import FacterBase
import socket
import struct
import fcntl
import array

#fcntl.ioctl flag come from /usr/include/linux/sockios.h

class Facter(FacterBase):
    def _init(self):
        self.interface_info_dict = self._get_interface_list()
    
    def _get_interface_list(self):
        """Provides a list of available network interfaces
           as a list of tuples (name, ip)"""
        max_iface = 32  # Maximum number of interfaces(Aribtrary)
        bytes = max_iface * 32
        is_32bit = (8 * struct.calcsize("P")) == 32  # Set Architecture
        struct_size = 32 if is_32bit else 40
    
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            names = array.array('B', '\0' * bytes)
            outbytes = struct.unpack('iL', fcntl.ioctl(
                s.fileno(),
                0x8912,  # SIOCGIFCONF
                struct.pack('iL', bytes, names.buffer_info()[0])
            ))[0]
            namestr = names.tostring()
            return dict([(namestr[i:i + 32].split('\0', 1)[0],
                    socket.inet_ntoa(namestr[i + 20:i + 24]))\
                    for i in range(0, outbytes, struct_size)])
    
        except IOError:
            raise IOError('Unable to call ioctl with SIOCGIFCONF')   
    
    def _get_interface_ip(self,interface_name):
        s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0X8915, struct.pack('256s', interface_name[:15]))[20:24])
        
    def _get_interface_mac(self,interface_name):
        s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return ".".join(["%02x"%ord(i) for i in fcntl.ioctl(s.fileno(), 0x8927, struct.pack('256s', interface_name[:15]))[18:24]])
    
    #def facter_interfaces(self):
        #with open("/proc/net/dev", "r") as f:
            #_ = f.readline()
            #_ = f.readline()
            #line = f.readline()
            #while line:
                #self.interface_list.append(line.split()[0].strip(":"))
                #line = f.readline()
        #return self.interface_list
    
    #def facter_interface_count(self):
        #return len(self.facter_interfaces())
    
    def __iter__(self):
        ret = ['interface_count', 'interfaces']
        for i in self.facter_interfaces:
            ret.append("%s_ip"%i)
            ret.append("%s_mac"%i)
        return iter(ret)
    
    def __getattr__(self,name):
        if name == "facter_interfaces":
            return self.interface_info_dict.keys()
        if name == "facter_interface_count":
            return len(self.interface_info_dict)
        elif name.endswith("_mac") and name.startswith("facter_"):
            interface_name = name.replace("_mac",'').split("_")[-1]
            return self._get_interface_mac(interface_name)
        elif name.endswith("_ip") and name.startswith("facter_"):
            interface_name = name.replace("_ip",'').split("_")[-1]
            return self.interface_info_dict.get(interface_name,None)
        else:
            raise AttributeError,"%s not implement"%name
    
    
    