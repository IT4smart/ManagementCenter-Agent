#!/usr/bin/python
import apt, json

class Packages(object):

    def __init__(self):
        print "Init package module"

    def get_installed_packages(self, mac, id):
        cache = apt.Cache()
        response = []

        for mypkg in cache.keys():
            if cache[mypkg].is_installed:
                pkg_version = apt.package.Version(cache[mypkg], cache[mypkg].candidate)
                response.append({'package': cache[mypkg].name , 'version': cache[mypkg].installed.version , 'mac' : str(mac) , 'id_command_jobs': str(id)})
                
        
        return json.dumps(response)
