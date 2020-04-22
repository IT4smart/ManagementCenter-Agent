#!/usr/bin/python3
import apt, json
import os

class Packages(object):

    def __init__(self, mac, id):
        print("Init package module")
        self.id = id
        self.mac = mac

    def get_installed_packages(self):
        cache = apt.Cache()
        response = []

        try:
            for mypkg in cache.keys():
                if cache[mypkg].is_installed:
                    pkg_version = apt.package.Version(cache[mypkg], cache[mypkg].candidate)
                    response.append({'package': cache[mypkg].name , 'version': cache[mypkg].installed.version , 'mac' : str(self.mac) , 'id_command_jobs': str(self.id)})
                
        except:
            response.append({'error': sys.exec_info()[0], 'mac': str(self.mac), 'id_command_jobs': str(self.id)})
        
        finally:
            cache.close()
            return json.dumps(response)
        
        
    def get_upgradable_packages(self):
        cache = apt.Cache()
        response = []
        
        try:
            # update the package list before we try to get all upgradable packages)
            cache.update()
            cache.open(None)
            
        
            for mypkg in cache.keys():
                if cache[mypkg].is_upgradable:
                    response.append({'package': cache[mypkg].name, 'mac': str(self.mac), 'id_command_jobs': str(self.id)})
        
        except:
            response.append({'error': sys.exec_info()[0], 'mac': str(self.mac), 'id_command_jobs': str(self.id)})
        
        finally:
            cache.close()
            return json.dumps(response)
