# -*- coding: utf-8 -*-

import json
import requests
import time
import psutil
import os
import platform
import fcntl
import socket
import struct
import configparser
import logging
from logging.config import fileConfig
import logging.handlers

# custom IT4smart packages
from plugins import Packages
from plugins import System

# set up configparser
dir_path = os.path.dirname(os.path.realpath(__file__))
config = configparser.ConfigParser()

# init logging
# fileConfig(dir_path + "/logging_config.ini")
log = logging.getLogger("management-agent-it4smart")

# read config
config.read(dir_path + "/config.ini")

# build base url with information from config file
base_url = (
    config.get("Main", "protocol")
    + "://"
    + config.get("Main", "server")
    + "/api/v1/"
)

def setup_logging(default_path='logging.json', default_level=logging.INFO, env_key='LOG_CFG'):
    """
        Setup logging configuration
    """
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = json.load(f)
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)

# get mac address
def getHwAddr(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    info = fcntl.ioctl(
        s.fileno(), 0x8927, struct.pack("256s", bytes(ifname, "utf-8")[:15])
    )
    return ":".join("%02x" % b for b in info[18:24])


# get ip address
def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(
        fcntl.ioctl(
            s.fileno(),
            0x8915,  # SIOCGIFADDR
            struct.pack("256s", bytes(ifname, "utf-8")[:15]),
        )[20:24]
    )


# get system uptime
def uptime():
    return time.time() - psutil.boot_time()


# reboot system
def reboot():
    # logging
    log.debug("Reboot device")

    os.system("sudo reboot")


def shutdown():
    # logging
    log.debug("Shutdown device")

    os.system("sudo shutdown -h now")


# get hostname
def hostname():
    # logging
    log.debug("Hostname: %s", platform.node())
    return platform.node()


def save_config(path, config):
    with open(path + "/config.ini", "wb") as configfile:
        config.write(configfile)


##################################################################
#
# Functions to communicate with management server
#
##################################################################


# set system uptime on management server
def set_device_uptime(mac, id):
    url = base_url + "device/" + mac + "/" + str(id) + "/uptime"

    # logging
    log.debug("Set uptime: %s", url)

    response = requests.put(url)
    log.debug(json.loads(response.read()))


def set_device_packages(mac, id):
    url = base_url + "device_package_data"

    # logging
    log.debug("URL to post device package data: %s", url)

    p = Packages.Packages(mac, id)
    p_result = p.get_installed_packages()

    response = requests.post(
        url, data=p_result, headers={"Content-Type": "application/json"}
    )

    # logging
    log.debug("Response status: %s", str(response.status_code))

    result_text = response.text
    result_text = result_text.encode("utf-8")

    # logging
    log.debug("Response text: %s", result_text)


def set_device_data(mac, id):
    # logging
    log.debug("Collect device data")
    url = base_url + "device_data"

    # logging
    log.debug("URL to post collected data: %s", url)

    o = System.System.Os()
    m = System.System.Hardware.Memory()
    n = System.System.Hardware.Network()
    c = System.System.Hardware.Cpu()

    # get all interfaces
    iface = n.interfaces()

    # get information for interface which is not loopback
    for iface2 in iface:
        if iface2 != "lo":
            log.debug("Network interface to collect data from: %s", iface2)
            iface_details = n.interface_details(iface2)

    json_data = []
    json_data.append(
        {
            "name": "architecture",
            "value": o.architecture(),
            "mac": str(mac),
            "idcommand_jobs": str(id),
        }
    )
    json_data.append(
        {
            "name": "kernel_version",
            "value": o.kernel_release(),
            "mac": str(mac),
            "idcommand_jobs": str(id),
        }
    )
    json_data.append(
        {
            "name": "memory_total",
            "value": m.total(),
            "mac": str(mac),
            "idcommand_jobs": str(id),
        }
    )
    json_data.append(
        {
            "name": "memory_free",
            "value": m.free(),
            "mac": str(mac),
            "idcommand_jobs": str(id),
        }
    )
    json_data.append(
        {
            "name": "net_ip",
            "value": iface_details[1],
            "mac": str(mac),
            "idcommand_jobs": str(id),
        }
    )
    json_data.append(
        {
            "name": "net_speed",
            "value": iface_details[0],
            "mac": str(mac),
            "idcommand_jobs": str(id),
        }
    )
    json_data.append(
        {
            "name": "net_subnetmask",
            "value": iface_details[2],
            "mac": str(mac),
            "idcommand_jobs": str(id),
        }
    )
    json_data.append(
        {
            "name": "cpu_cores",
            "value": c.physical_core_count(),
            "mac": str(mac),
            "idcommand_jobs": str(id),
        }
    )
    json_data.append(
        {
            "name": "cpu_family",
            "value": c.brand(),
            "mac": str(mac),
            "idcommand_jobs": str(id),
        }
    )
    json_data.append(
        {
            "name": "cpu_speed",
            "value": c.hz_advertised(),
            "mac": str(mac),
            "idcommand_jobs": str(id),
        }
    )

    # logging
    log.debug("Collected device data: %s", json_data)

    response = requests.post(
        url, data=json.dumps(json_data), headers={"Content-Type": "application/json"}
    )

    # logging
    log.debug("Response status: %s", str(response.status_code))

    result_text = response.text
    result_text = result_text.encode("utf-8")

    # logging
    log.debug("Response text: %s", result_text)


def main():
    # setup the enviroment
    setup_logging(dir_path + "/logging.json")

    # start logging
    log.info("Start logging")

    # get interface
    n = System.System.Hardware.Network()

    # get all interfaces
    iface = n.interfaces()
    # get information for interface which is not loopback
    for iface2 in iface:
        if iface2 != "lo":
            network_interface = iface2
            log.info("Network device found: %s", network_interface)

    # endless loop for running as systemd service
    while True:
        # logging
        log.info("Read settings from: %s/config.ini", dir_path)

        # read config
        config.read(dir_path + "/config.ini")

        # build base url with information from config file
        base_url = (
            config.get("Main", "protocol")
            + "://"
            + config.get("Main", "server")
            + "/api/v1/"
        )

        # logging
        log.info("Base URL for requests is: %s", base_url)

        # wait some time
        time.sleep(config.getfloat("Main", "timeout"))

        # logging
        log.debug("Client firstboot state: %s", config.get("Client", "firstboot"))

        # only check for jobs if device is registered
        if int(config.get("Client", "firstboot")) == 0:
            try:
                # logging
                log.debug("Device is in firstboot mode")

                url = base_url + "device/" + getHwAddr(network_interface)

                json_data = {}
                json_data["ipAddress"] = get_ip_address(network_interface)

                r = requests.put(
                    url,
                    json=json_data,
                    headers={"Content-Type": "application/json"},
                    verify=False,
                )

                if r.status_code == 200:
                    log.info("Update device information successfully.")

                url = base_url + "device/" + getHwAddr(network_interface) + "/configure"

                # logging
                log.debug("Start configure device with request: %s", url)

                r = requests.put(url, verify=False)

                if r.status_code == 202:
                    data = r.json()

                    # logging
                    log.debug("Response from requestings jobs: %s", data)

                    config.set("Client", "firstboot", "1")
                    save_config(dir_path, config)
            except requests.exceptions.RequestException as e:
                log.error("Error [%s]", e)
        else:
            log.debug("Nothing to do")


if __name__ == "__main__":
    main()
