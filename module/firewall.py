import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import base
import time
import hashlib
from subprocess import Popen
from subprocess import PIPE
from common.attribute import Attribute

class FirewallRule(base.Module):

    def __init__(self):
        self.ruleprefix = 'vanilla_'

    def action_show(self, params):
        args = 'netsh advfirewall firewall show rule'.split()
        args.append('name=' + params['name'] if 'name' in params else 'all')

        process = Popen(args, stdout=PIPE)
        output = process.stdout.read()

        rulemap = Attribute(rulemap=[])

        try:
            if output:
                records = [info for info in output.split('\r\n\r\n') if self.ruleprefix in info]

                for record in records:
                    attrs = record.strip().split('\r\n')

                    name, remoteip, localport = attrs[0].split(':')[1].strip(), \
                        attrs[7].split(':')[1].strip(), attrs[9].split(':')[1].strip('\xa1 ')

                    rulemap.rulemap.append({
                        'name' : name,
                        'localport' : localport,
                        'remoteip' : remoteip
                    })
        except Exception, e:
            pass

        return rulemap


    def action_add(self, params):
        rulename = self.__generate_rulename(params)

        process = Popen(['netsh', 'advfirewall', 'firewall', 'add', 'rule',
            'name=' + rulename,
            'localport=' + params['localport'],
            'remoteip=' + params['remoteip'],
            'dir=in',
            'action=allow',
            'protocol=tcp'])
        process.wait()

        return Attribute(status=process.returncode == 0)

    def action_remove(self, params):
        if 'name' not in params:
            rulename = self.__generate_rulename(params)
        else:
            rulename = params['name']

        process = Popen(['netsh', 'advfirewall', 'firewall', 'delete', 'rule',
            'name=' + rulename])
        process.wait()

        return Attribute(status=process.returncode == 0)

    def __generate_rulename(self, params):
        FORMAT = 'tcp:{}:{}'.format(params['localport'], params['remoteip'])
        identifier = hashlib.md5(FORMAT).hexdigest()

        return self.ruleprefix + identifier

'''
    firewall = FirewallRule()
    firewall.action_add({'localport' : 8080, 'remoteip' : '127.0.0.1'})
    firewall.action_show({})
    firewall.action_remove({'name' : 'vanilla_4f8504bf1ebfe335d722cc73f9d63ba3'})
    firewall.action_show({})
'''
