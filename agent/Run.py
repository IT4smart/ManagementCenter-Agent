# -*- coding: utf-8 -*-

import urllib, json, requests
import time
import psutil, os, platform
import fcntl, socket, struct
import ConfigParser
import logging 
from logging.config import fileConfig
import logging.handlers 

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
    # logging
    log.debug('Reboot device')
    
    os.system('sudo reboot')
    
def shutdown():
    # logging
    log.debug('Shutdown device')
    
    os.system('sudo shutdown -h now')
    
# get hostname
def hostname():
    # logging
    log.debug('Hostname: %s', platform.node())
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
    
    # logging
    log.debug('Set uptime: %s', url)
    
    response = urllib.urlopen(url)
    #print json.loads(response.read())
    
# set device state
def set_device_state(mac, id):
    url = base_url + "device_state/online/" + mac + "/" + str(id)
    # logging
    log.debug('URL to post result: %s', url)
    
    response = urllib.urlopen(url)
    print json.loads(response.read())
    
# reboot system
def set_device_reboot(id):
    url = base_url + "device_reboot/" + str(id)
    
    # logging
    log.debug('URL to post that device is rebooting: %s', url)
    
    response = urllib.urlopen(url)
    #print json.loads(response.read())
    reboot()
    
def set_device_shutdown(id):
    url = base_url + "device_shutdown/" + str(id)
    
    # logging
    log.debug('URL to post that device is shutingdown: %s', url)
    
    response = urllib.urlopen(url)
    #print json.loads(response.read())
    shutdown()
    
def set_device_packages(mac, id):
    url = base_url + "device_package_data"
    
    # logging
    log.debug('URL to post device package data: %s', url)
    
    p = Packages.Packages(mac, id)
    p_result = p.get_installed_packages()
    
    response = requests.post(url, data=p_result, headers={'Content-Type': 'application/json'})
    
    # logging
    log.debug('Response status: %s', str(response.status_code))
    
    result_text = response.text
    result_text = result_text.encode('utf-8')
    
    # logging
    log.debug('Response text: %s', result_text)
    

def set_device_data(mac, id):
    # logging
    log.debug('Collect device data')
    url = base_url + "device_data"
    
    # logging
    log.debug('URL to post collected data: %s', url)
    
    o = System.System.Os()
    m = System.System.Hardware.Memory()
    n = System.System.Hardware.Network()
    c = System.System.Hardware.Cpu()
    
    # get all interfaces
    iface = n.interfaces()
    
    # get information for interface which is not loopback
    for iface2 in iface:
        if iface2 != "lo":
            log.debug('Network interface to collect data from: %s', iface2)
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

    # logging
    log.debug('Collected device data: %s', json_data)
    
    response = requests.post(url, data=json.dumps(json_data), headers={'Content-Type': 'application/json'})
    
    # logging
    log.debug('Response status: %s', str(response.status_code))
    
    result_text = response.text
    result_text = result_text.encode('utf-8')
    
    # logging
    log.debug('Response text: %s', result_text)
    
    
def register_device(mac, hostname):
    url = base_url + "device_register/"+ str(mac) + "/" + hostname
    
    # logging
    log.debug('Register device at management point: %s', url)
    
    response = urllib.urlopen(url)
    print json.loads(response.read())
    
def get_register_state(mac):
    url = base_url + "device_register_state/" + str(mac)
    
    # logging
    log.debug('Ask api for register state: %s', url)
    
    # response from request
    response = urllib.urlopen(url)
    return json.loads(response.read())
    
def set_register_state(id, state):
    url = base_url + "device_register_state/" + str(id) + "/" + state
    
    # logging
    log.debug('Send response to api: %s', url)
    
    response = urllib.urlopen(url)
    print json.loads(response.read())
    
if __name__ == '__main__':

    # setup the enviroment
    # set up configparser
    dir_path = os.path.dirname(os.path.realpath(__file__))
    config = ConfigParser.ConfigParser()

    # init logging
    fileConfig(dir_path + '/logging_config.ini')
    log = logging.getLogger('management-agent-it4s')

    # start logging
    log.info('Start logging')
    
    # get interface
    n = System.System.Hardware.Network()

    # get all interfaces
    iface = n.interfaces()
    # get information for interface which is not loopback
    for iface2 in iface:
        if iface2 != "lo":
            network_interface = iface2
            log.info('Network device found: %s', network_interface)
            
    # endless loop for running as systemd service
    while True:
        # logging
        log.info('Read settings from: %s/config.ini', dir_path)
        
        # read config
        config.read(dir_path + '/config.ini')
        
        # build base url with information from config file
        base_url = config.get('Main', 'protocol') + "://" + config.get('Main', 'server') + "/api/v1/"
        
        # logging
        log.info('Base URL for requests is: %s', base_url)
        
        # wait some time
        time.sleep(config.getfloat('Main', 'timeout'))
        
        # logging
        log.debug('Client register state: %s', config.get('Client', 'registered'))
        
        # only check for jobs if device is registered
        if int(config.get('Client', 'registered')) == 2:
            # logging
            log.debug('Device is registered and requesting for jobs')
            
            url = base_url + "job/" + getHwAddr(network_interface)
            
            # logging
            log.debug('Getting jobs from: %s', url)
            
            response = urllib.urlopen(url)
            data = json.loads(response.read())
            
            # logging
            log.debug('Response from requestings jobs: %s', data)
            
            # handle jobs
            if data['command'] == 'get device state':
                log.info('get device state')
                time.sleep(5)
                set_device_state(getHwAddr(network_interface),  data['idcommand_jobs'])
            elif data['command'] == 'get uptime':
                # logging
                log.info('get device uptime')
                time.sleep(5)
                # logging
                log.debug('System uptime of %d seconds', uptime())
                set_device_uptime(getHwAddr(network_interface),  data['idcommand_jobs'])
            elif data['command'] == 'sudo reboot':
                # logging
                log.info('Device reboot')
                time.sleep(5)
                set_device_reboot(data['idcommand_jobs'])
            elif data['command'] == 'shutdown':
                # logging
                log.info('Device shutdown')
                time.sleep(5)
                set_device_shutdown(data['idcommand_jobs'])            
            elif data['command'] == 'get_package_data':
                # logging
                log.info('Device get package data')
                time.sleep(5)
                set_device_packages(getHwAddr(network_interface),  data['idcommand_jobs'])
            elif data['command'] == 'get_device_data':
                # logging
                log.info('Get device data')
                time.sleep(5)
                set_device_data(getHwAddr(network_interface),  data['idcommand_jobs'])
            else:
                log.info('No jobs found')
            
        # add support to look if device get registered or any error occured.
        elif config.get('Client', 'registered') == '1':
            #logging
            log.info('Device will be added to the system')
            
            # wait 5 seconds
            time.sleep(5)
            
            data = get_register_state(getHwAddr(network_interface))
            
            # job is waiting for response
            if data[0]['state'] == 'wait_resp':
                # logging
                log.debug('Device is queued for registering and is waiting for a response from this client')
                
                # set client as registered
                config.set('Client', 'registered', '2')
                save_config(dir_path, config)
                
                # send response to api that we saved the current state
                log.debug('Send response to api that we saved the current state')
                set_register_state(data[0]['iddevice_registering_jobs'], 'done')
                
                # logging
                log.info('Device is now registered at management console')
        elif config.get('Client', 'registered') == '0':
            # Client is not registered at the management software
            # logging
            log.info('Device is not registered. Start registering it...')
            
            time.sleep(5)
            
            # logging
            log.debug('Data for registering. Hostname: %s, MAC: %s', hostname(), getHwAddr(network_interface))
            register_device(getHwAddr(network_interface), hostname())
            
            # logging 
            log.debug('Set setting Client\registered to 1')
            config.set('Client', 'registered', '1')
            
            # logging
            log.debug('Save the config.')
            save_config(dir_path, config)
        else:
            log.debug('Nothing to do')
            