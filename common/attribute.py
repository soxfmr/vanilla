import json


class Attribute(object):

    def __init__(self, **kargs):
        if kargs:
            for key, value in kargs.items():
                self.__dict__[key] = value

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
