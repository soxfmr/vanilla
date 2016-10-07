import socket
from common.attribute import Attribute

INDEX_COMMAND_NAME = 0
INDEX_COMMAND_PARAMS = 1
INDEX_COMMAND_HELP = 2
INDEX_COMMAND_ENTITIES = 3

class Teleport(object):

    def __init__(self):
        pass

class CommandDispatcher(object):

    def __init__(self, commands):
        self.map = self.__build(commands)

    def __build(self, commands):
        '''
        +---------------------------------------+
        | <name>:<arguments>:<help>:<?entities> |
        +---------------------------------------+
        Example:
        {
            'exit' : ('', exit), # <=== top-level menu, will invoke the callbcak function

            'PortForward' : [
                '-a:[lport] [raddr] [rport]:Forward a local port to remote address port',
                '-d:[lport]',
                '-l:Show forward table',

                ( '--verify:[port]:verfiy port range', verify ), # <=== sub menu with callbcak function
                ( '-V::show module version', show_version )
            ]
        }
        '''
        result = {}

        for name, command in commands.items():
            if isinstance(command, (list, tuple)):
                '''
                ( ':[argumens]:', function_ptr )
                treat as a top-level menu, and put it into a new list object
                '''
                toplevel = isinstance(command, tuple)
                if toplevel:
                    command = [command]

                result[name] = self.__get_submenu(command, toplevel)
            else:
                raise ValueError('Invalid commands')

        return result

    def __get_submenu(self, params, toplevel=False):
        result = []
        for command in params:
            if isinstance(command, (tuple, str)):
                menu = Attribute(name='', params=[], help='', callback=None,
                    entities=[], toplevel=toplevel)
                # help message
                message = []

                # top level command or with the callback function
                if isinstance(command, tuple):
                    command, menu.callback = command

                slices = command.split(':')
                length = len(slices)

                # command name
                if slices[INDEX_COMMAND_NAME]:
                    menu.name = slices[INDEX_COMMAND_NAME]
                    message.append(menu.name)
                elif not toplevel:
                    raise ValueError('Got command without unique name in {}'.format( command ))

                # command params
                if length >= 2 and slices[INDEX_COMMAND_PARAMS]:
                    args = slices[INDEX_COMMAND_PARAMS].split()
                    menu.params = map(lambda param: param.strip('[]'), args)
                    # validate param name, should't be null
                    for param in menu.params:
                        if not param:
                            raise ValueError('Empty param name in {}'.format( command ))

                    message += args

                # command entities
                if length >= 4 and slices[INDEX_COMMAND_ENTITIES]:
                    entities = filter(lambda entity: entity, slices[INDEX_COMMAND_ENTITIES].split('?'))
                    menu.entities = entities

                    message.append('or <{}>'.format( '|'.join( entities ) ))

                # command help in the end of line
                if length >= 3 and slices[INDEX_COMMAND_HELP]:
                    message.append('- {}'.format( slices[INDEX_COMMAND_HELP] ))

                menu.help = ' '.join(message)

                result.append(menu)
            else:
                raise ValueError('Invalid command format, should be string or tuple')

        return result

    def dispatch(self, data):
        pass

    def list(self):
        if self.map:
            print ','.join( self.map.keys() )

    def show(self, module):
        if self.map and module in self.map:
            for menu in self.map[module]:
                print menu.help

class Workbench(object):

    def __init__(self, dispatcher):
        self.currentId = 0
        self.prompt = 'vs'
        self.dispatcher = dispatcher

    def forge(self):
        try:
            while True:
                command = raw_input('[{}:{}]>> '.format(self.prompt, self.currentId))
                # dispatcher.dispatch(command)
                if 'list' in command:
                    self.dispatcher.list()
                elif 'show' in command:
                    self.dispatcher.show(command.split()[1])

        except KeyboardInterrupt:
            pass

def main():
    commands = {
        'forward' : [
            '-a:[listenport] [connectaddress] [connectport]',
            '-d:[listenport]:Remove a forward rule specified by listen port',
            '-l::Show forward table'
        ],
        'firewall' : [
            '-a:[localport] [remoteip]:Append a firewall rule that open the port for remote ip',
            '-d:[name]:Remove a firewall rule:?all',
            '-s:[name]:Show the detail information of the rule',
            '-l::Show firewall rules (partial)'
        ]
    }
    workbench = Workbench(dispatcher=CommandDispatcher(commands))
    workbench.forge()

if __name__ == '__main__':
    main()
