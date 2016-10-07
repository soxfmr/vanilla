import json


class Attribute(object):

    def __init__(self, **kargs):
        if kargs:
            for key, value in kargs.items():
                self.__dict__[key] = value

    def __setattr__(self, name, value):
    	self.__dict__[name] = value

    def __getattr__(self, name):
        return self.__dict__[name] if name in self.__dict__ else None

    def __getitem__(self, name):
    	return self.__getattr__(name)

    def __setitem__(self, name, value):
    	self.__setattr__(name, value)

    def fromJson(self, data):
        if not data:
            return

        attrs = json.loads(data)
        for key, value in attrs.items():
            self.__dict__[key] = value

    def toJson(self):
        return json.dumps(self.__dict__)

    def __str__(self):
        return self.toJson()
