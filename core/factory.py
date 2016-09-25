import logging


class ModuleFactory(object):
    modules = []

    @staticmethod
    def addModule(module):
        ModuleFactory.modules.append( module )

        logging.info('Module {} plug-in'.format( module['name'] ))

    @staticmethod
    def createModule(module):
        for m in ModuleFactory.modules:
            if m['id'] == module:
                return m['addr']()
        return None

    @staticmethod
    def loadModules(modules):
        ModuleFactory.modules = modules

        logging.info('Totally {} modules loaded'.format( len(modules) ))
