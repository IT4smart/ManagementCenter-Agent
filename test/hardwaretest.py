import unittest
import re

from agent.Run import getHwAddr, get_ip_address
from agent.plugins import System


class TestHardware(unittest.TestCase):
    def test_mac_address(self):
        """
        Test if there will be a valid mac address
        """
        n = System.System.Hardware.Network()
        iface = n.interfaces()
        for iface2 in iface:
            if iface2 != "lo":
                network_interface = iface2

        macAddress = getHwAddr(network_interface)
        print("MAC-Address: {}".format(macAddress))
        pattern = re.compile("[0-9a-f]{2}([-:]?)[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$")
        pattern.fullmatch(macAddress)
        self.assertIsNotNone(pattern)

    def test_ip_address(self):
        """
        Test if there will be a valid ip address
        """
        n = System.System.Hardware.Network()
        iface = n.interfaces()
        for iface2 in iface:
            if iface2 != "lo":
                network_interface = iface2

        ipAddress = get_ip_address(network_interface)
        print("IP-Address: {}".format(ipAddress))
        pattern = re.compile("^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")
        pattern.fullmatch(ipAddress)
        self.assertIsNotNone(pattern)


if __name__ == "__main__":
    unittest.main()
