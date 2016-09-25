class Module(object):

    def __init__(self, prefix='action_'):
        self.prefix = prefix
        self.actions = self.__load()
        self.upper = len(self.actions)

    def __load(self):
        i = 1
        methods = []
        actions = [name for name in dir(self) if self.prefix in name].sort()

        for action in actions:
            method = getattr(self, action)
            methods.append({
                'id'    : i,
                'name'  : action,
                'addr'  : method,
                'desc'  : method.__doc__
            })
            i += 1

        return methods

    def execute(self, action, params):
        if action < self.upper:
            method = self.actions[action]
            return method(params)

        return False
