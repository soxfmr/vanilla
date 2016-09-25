import json
import logging
from core.server import Server
from core.logger import initlog
from core.factory import ModuleFactory
from pam.rsa import RSAEncryptor
from middleware.auth import Auth
from middleware.shield import Shield


def import_modules():
    instance    = __import__('module')
    baseMod     = getattr(instance, 'Module')
    # List all of modules
    modules     = dir(instance)

    i = 1
    availableMods = []

    for module in modules:
        addr = getattr(instance, module)
        try:
            if issubclass(addr, baseMod) and module != 'Module':
                availableMods.append({
                    'id'    : i,
                    'name'  : module,
                    'addr'  : addr,
                    'desc'  : addr.__doc__
                })
                i += 1
        except TypeError:
            pass

    return availableMods

def main():
    try:
        initlog()

        with open('.env', 'r') as handle:
            env = json.loads(handle.read())

        modmap = import_modules()
        ModuleFactory.loadModules(modmap)

        middlewares = {
            'shield' : Shield(),
            'auth' : Auth( env['password'], RSAEncryptor(env['key']) ) }

        server = Server(addr=('0.0.0.0', 8080), middlewares=middlewares)
        server.start()
        server.wait()
    except IOError, e:
        logging.error('IO Expection: %s', str(e))
    except KeyboardInterrupt:
        logging.info('User abort')
    finally:
        try:
            if server: server.close()
        except:
            pass
        logging.info('Program exit')

if __name__ == '__main__':
    main()
