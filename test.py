#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib, json, requests
import fcntl, socket, struct
import time
import psutil
import debinterface.interfaces 

# custom IT4S packages
from plugins import Packages
from plugins import System

# get mac address
def getHwAddr(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    info = fcntl.ioctl(s.fileno(), 0x8927,  struct.pack('256s', ifname[:15]))
    return ':'.join(['%02x' % ord(char) for char in info[18:24]])

def set_device_data(mac, id):
    url = "http://192.168.178.39/verwaltungskonsole/api/v1/device_data"
    print url
    o = System.System.Os()
    m = System.System.Hardware.Memory()
    n = System.System.Hardware.Network()
    c = System.System.Hardware.Cpu()
    
    # get all interfaces
    iface = n.interfaces()
    
    # get information for interface which is not loopback
    for iface2 in iface:
        if iface2 != "lo":
            iface_details = n.interface_details(iface2)
    
    json_data = []
    json_data.append({'name': 'architecture', 'value': o.architecture()})
    json_data.append({'kernel_version': o.kernel_release()})
    json_data.append({'memory_total': m.total()})
    json_data.append({'memory_free': m.free()})
    json_data.append({'net_ip': iface_details[1]})
    json_data.append({'net_speed': iface_details[0]})
    json_data.append({'net_subnetmask': iface_details[2]})
    json_data.append({'cpu_cores': c.physical_core_count()})
    json_data.append({'cpu_family': c.brand()})
    json_data.append({'cpu_speed': c.hz_advertised()})
    print json_data
    #response = requests.post(url, data=p_result, headers={'Content-Type': 'application/json'})
    #print response.status_code
    #result_text = response.text
    #result_text = result_text.encode('utf-8')
    #print result_text
    

    
    
# Main
#url = "http://192.168.178.39/verwaltungskonsole/api/v1/job/" + getHwAddr('ens32')
#print url
#response = urllib.urlopen(url)
#data = json.loads(response.read())
#if data['command'] == 'get_device_data':
#    time.sleep(5)
set_device_data(getHwAddr('ens32'),  1)

                

