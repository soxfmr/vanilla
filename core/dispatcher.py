import logging
from package import isnewpackage
from package import PackageBuilder
from factory import ModuleFactory


class Dispatcher(object):

    def __init__(self, encryptor):
        self.encryptor = encryptor
        self.lastpkg = None
        self.channel = None

    def setchannel(self, channel):
        self.channel = channel

    def dispatch(self, data):
        if isnewpackage(data):
            if self.lastpkg:
                logging.warn('New package present, previous package deprecated.')
            self.lastpkg = PackageBuilder(data, self.encryptor)
        else:
            if not self.lastpkg:
                logging.warn('Incomplete package, discarded.')
                return
            self.lastpkg.append(data)

        if self.lastpkg.iscomplete():
            module, action, params = self.lastpkg.unpack()

            module = ModuleFactory.createModule(module)
            result = module.execute(action, params)

            if result: self.channel.put( lastpkg.build(data) )

            # marked
            self.lastpkg = None
