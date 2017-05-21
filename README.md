# z-agent
z-agent实现zabbix的trapper的发送，主机信息的采集，单机任务处理

## 构成
 - zabbix-sender
 - facter
 - checker
 - discovery
 - executor
 - stats
 
## 注意事项
 这是一个过渡版本，会兼容zabbix，使用zabbix协议跟zabbix server通讯，在使用这个版本的时候需要在zabbix server上增加trapper的数量。
