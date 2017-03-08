#!/usr/bin/env python
# -*- coding:utf8 -*-

''' import module '''
import protobix

''' create DataContainer, providing data_type, zabbix server and port '''
zbx_container = protobix.DataContainer("items", "172.16.5.220", 10051)
''' set debug '''
zbx_container.set_debug(True)
zbx_container.set_verbosity(True)

''' Add items one after the other '''
hostname="localhost" #hostname ying shi zbx li de mingzi
item="trap1"   #item shi shoudong chuanjian
value="test-only"
zbx_container.add_item( hostname, item, value)

''' or use bulk insert '''
data = {
    "172.16.5.238": {
        "trap1": "test-only",
    },
    "myhost2": {
        "my.zabbix.item1": 0,
        "my.zabbix.item2": "item string"
    }
}
data={}
zbx_container.add(data)

''' Send data to zabbix '''
ret = zbx_container.send(zbx_container)
''' If returns False, then we got a problem '''
if not ret:
    print "Ooops. Something went wrong when sending data to Zabbix"

print "Everything is OK"