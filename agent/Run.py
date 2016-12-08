#!/usr/bin/python

import urllib, json, requests
import time
import psutil, os, platform
import fcntl, socket, struct
import ConfigParser

# custom IT4S packages
from plugins import Packages
from plugins import System

# get mac address
def getHwAddr(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    info = fcntl.ioctl(s.fileno(), 0x8927,  struct.pack('256s', ifname[:15]))
    return ':'.join(['%02x' % ord(char) for char in info[18:24]])

# get ip address
def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])

# get system uptime
def uptime():
    return time.time() - psutil.boot_time()

# reboot system
def reboot():
    os.system('sudo reboot')
    
def shutdown():
    os.system('sudo shutdown -h now')
    
# get hostname
def hostname():
    return platform.node()

def save_config(path, config):
    with open(path + '/config.ini', 'wb') as configfile:
        config.write(configfile)
    
##################################################################
#
# Functions to communicate with management server
#
##################################################################

# set system uptime on management server
def set_device_uptime(mac, id):
    url = base_url + "device_uptime/" + str(uptime()) + "/" + mac + "/" + str(id)
    print "Set uptime: " + url
    response = urllib.urlopen(url)
    print json.loads(response.read())
    
# set device state
def set_device_state(mac, id):
    url = base_url + "device_state/online/" + mac + "/" + str(id)
    print url
    response = urllib.urlopen(url)
    print json.loads(response.read())
    
# reboot system
def set_device_reboot(id):
    url = base_url + "device_reboot/" + str(id)
    print url
    response = urllib.urlopen(url)
    print json.loads(response.read())
    reboot()
    
def set_device_shutdown(id):
    url = base_url + "device_shutdown/" + str(id)
    print url
    response = urllib.urlopen(url)
    print json.loads(response.read())
    shutdown()
    
def set_device_packages(mac, id):
    url = base_url + "device_package_data"
    print url
    p = Packages.Packages()
    p_result = p.get_installed_packages(mac, id)
    #print p_result
    response = requests.post(url, data=p_result, headers={'Content-Type': 'application/json'})
    print response.status_code
    result_text = response.text
    result_text = result_text.encode('utf-8')
    print result_text

def set_device_data(mac, id):
    url = base_url + "device_data"
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
    json_data.append({'name': 'architecture', 'value': o.architecture(), 'mac': str(mac), 'idcommand_jobs': str(id)})
    json_data.append({'name': 'kernel_version', 'value': o.kernel_release(), 'mac': str(mac), 'idcommand_jobs': str(id)})
    json_data.append({'name': 'memory_total', 'value': m.total(), 'mac': str(mac), 'idcommand_jobs': str(id)})
    json_data.append({'name': 'memory_free', 'value': m.free(), 'mac': str(mac), 'idcommand_jobs': str(id)})
    json_data.append({'name': 'net_ip', 'value': iface_details[1], 'mac': str(mac), 'idcommand_jobs': str(id)})
    json_data.append({'name': 'net_speed', 'value': iface_details[0], 'mac': str(mac), 'idcommand_jobs': str(id)})
    json_data.append({'name': 'net_subnetmask', 'value': iface_details[2], 'mac': str(mac), 'idcommand_jobs': str(id)})
    json_data.append({'name': 'cpu_cores', 'value': c.physical_core_count(), 'mac': str(mac), 'idcommand_jobs': str(id)})
    json_data.append({'name': 'cpu_family', 'value': c.brand(), 'mac': str(mac), 'idcommand_jobs': str(id)})
    json_data.append({'name': 'cpu_speed', 'value': c.hz_advertised(), 'mac': str(mac), 'idcommand_jobs': str(id)})

    response = requests.post(url, data=json.dumps(json_data), headers={'Content-Type': 'application/json'})
    print response.status_code
    result_text = response.text
    result_text = result_text.encode('utf-8')
    print result_text
    
def register_device(mac, hostname):
    url = base_url + "device_register/"+ str(mac) + "/" + hostname
    print url
    response = urllib.urlopen(url)
    print json.loads(response.read())
    
def get_register_state(mac):
    url = base_url + "device_register_state/" + str(mac)
    print url
    response = urllib.urlopen(url)
    return json.loads(response.read())
    
def set_register_state(id, state):
    url = base_url + "device_register_state/" + str(id) + "/" + state
    print url
    response = urllib.urlopen(url)
    print json.loads(response.read())
    
if __name__ == '__main__':

    # set up configparser
    dir_path = os.path.dirname(os.path.realpath(__file__))
    config = ConfigParser.ConfigParser()
    
    # get interface
    n = System.System.Hardware.Network()

    # get all interfaces
    iface = n.interfaces()
    # get information for interface which is not loopback
    for iface2 in iface:
        if iface2 != "lo":
            network_interface = iface2
    
    # endless loop for running as systemd service
    while True:
        config.read(dir_path + '/config.ini')
        base_url = config.get('Main', 'protocol') + "://" + config.get('Main', 'server') + "/api/v1/"
        time.sleep(config.getfloat('Main', 'timeout'))
        
        # only check for jobs if device is registered
        if config.get('Client', 'registered') == 2:
            url = base_url + "job/" + getHwAddr(network_interface)
            print url
            response = urllib.urlopen(url)
            data = json.loads(response.read())
            print data
            
            
        if data['command'] == 'get device state':
            time.sleep(5)
            set_device_state(getHwAddr(network_interface),  data['idcommand_jobs'])
        elif data['command'] == 'get uptime':
            time.sleep(5)
            print 'System uptime of %d seconds' % (uptime())
            set_device_uptime(getHwAddr(network_interface),  data['idcommand_jobs'])
        elif data['command'] == 'sudo reboot':
            time.sleep(5)
            set_device_reboot(data['idcommand_jobs'])
        elif data['command'] == 'shutdown':
            time.sleep(5)
            set_device_shutdown(data['idcommand_jobs'])            
        elif data['command'] == 'get_package_data':
            time.sleep(5)
            set_device_packages(getHwAddr(network_interface),  data['idcommand_jobs'])
        elif data['command'] == 'get_device_data':
            time.sleep(5)
            set_device_data(getHwAddr(network_interface),  data['idcommand_jobs'])
        elif config.get('Client', 'registered') == '0':
            # Client is not registered at the management software
            time.sleep(5)
            register_device(getHwAddr(network_interface), hostname())
            config.set('Client', 'registered', '1')
            save_config(dir_path, config)
        # add support to look if device get registered or any error occured.
        elif config.get('Client', 'registered') == '1':
            time.sleep(5)
            data = get_register_state(getHwAddr(network_interface))
            
            # job is waiting for response
            if data[0]['state'] == 'wait_resp':
                config.set('Client', 'registered', '2')
                save_config(dir_path, config)
                set_register_state(data[0]['iddevice_registering_jobs'], 'done')
        else:
            print 'No jobs found'
    
