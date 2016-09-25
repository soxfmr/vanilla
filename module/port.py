import base
from subprocess import Popen
from subprocess import PIPE

class PortForward(base.Module):

    def __init__(self):
        pass

    def action_show(self, params):
        args = 'netsh interface portproxy show all'.split()
        process = Popen(args, stdout=PIPE)

        result = process.stdout.read()

    def action_add(self, params):
        pass

    def action_remove(self, params):
        pass
