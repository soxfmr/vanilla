import logging


class ModuleFactory(object):
    modules = []

    @staticmethod
    def addModule(name, info):
        ModuleFactory.modules[name] = info

        logging.info('Module {} plug-in'.format( name ))

    @staticmethod
    def createModule(name):
        if name in ModuleFactory.modules:
            module = ModuleFactory.modules[name]
            return module['addr']()
            
        return None

    @staticmethod
    def loadModules(modules):
        ModuleFactory.modules = modules

        logging.info('Totally {} modules loaded'.format( len(modules) ))
