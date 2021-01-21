from Solution.lib import UsecaseBase
from Solution.lib.usecase import Usecase

class Demo(Usecase):
    __usecase__ = 'demo'
    def __init__(self, user):
        self.network = None
        self.endpoints = None
        super().__init__(user)

    def initialize(self, network=None, endpoints=None, usecase_id=None):
        print('Initialized %s with network %s and endpoints %s'%(
            self.__usecase__, network, endpoints))
        self.network = network
        self.endpoints = endpoints
        super().initialize(usecase_id)

    def create(self, network, endpoints, user=None):
        self.network = network
        self.endpoints = endpoints
        super().create(user)

    def delete(self):
        self.network = None
        self.endpoints = None
        super().delete()

    def dump(self):
        return {"network": self.network, "endpoints": self.endpoints}
