from abc import ABCMeta

class UsecaseBase(object):
    @classmethod
    def get_usecases(cls):
        usecases = dict()
        return cls._get_usecases(cls, usecases)

    @classmethod
    def _get_usecases(cls, obj, usecases):
        for c in obj.__subclasses__():
            if getattr(c, "__usecase__", None):
                usecases[c.__usecase__] = c
            if c.__subclasses__():
                cls._get_usecases(c, usecases)
        return usecases

    def initialize(self):
        pass

    def create(self):
        pass

    def delete(self):
        pass

class AuthBase(object):
    @classmethod
    def get_auth_cls(cls):
        if len(cls.__subclasses__()) != 1:
            raise Exception("Expecting one Auth library, observed %s"%(
                cls.__subclasses__()))
        return cls.__subclasses__()[0]

    def get_auth_h(self, username, password, project):
        pass
