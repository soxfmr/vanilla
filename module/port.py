import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import base
from subprocess import Popen
from subprocess import PIPE
from common.attribute import Attribute

class PortForward(base.Module):

    def __init__(self):
        pass

    def action_show(self, params):
        args = 'netsh interface portproxy show all'.split()
        process = Popen(args, stdout=PIPE)

        portmap = Attribute(portmap=[])

        output = process.stdout.readlines()
        for record in output:
            record = record.strip()
            try:
                listenaddress, listenport, \
                    connectaddress, connectport = record.split()

                listenport = int(listenport)
                connectport = int(connectport)

                portmap.portmap.append({
                    'listenaddress' : listenaddress,
                    'listenport' : listenport,
                    'connectaddress' : connectaddress,
                    'connectport' : connectport
                })
            except:
                continue

        return portmap

    def action_add(self, params):
        process =  Popen(['netsh', 'interface', 'portproxy', 'add', 'v4tov4',
            'listenport=%d' % params['listenport'],
            'connectaddress=' + params['connectaddress'],
            'connectport=%d' % params['connectport'],
            'protocol=tcp'], stdout=PIPE)
        process.wait()

        return Attribute(status=process.returncode == 0)

    def action_remove(self, params):
        process =  Popen(['netsh', 'interface', 'portproxy', 'delete', 'v4tov4',
            'listenport=%d' % params['listenport'],
            'protocol=tcp'], stdout=PIPE)
        process.wait()

        return Attribute(status=process.returncode == 0)

'''
    # REQUIRE ADMINISTRATOR PRIVILEGES
    forward = PortForward()
    forward.action_add({'listenport' : 80, 'connectaddress' : '127.0.0.1', 'connectport' : 8080})
    print forward.action_show(None)
    forward.action_remove({'listenport' : 80})
    print forward.action_show(None)
'''
