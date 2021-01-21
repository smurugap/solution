from Solution.lib import UsecaseBase
from Solution.lib.usecase import Usecase

class Demo2(Usecase):
    __usecase__ = 'vEPC'
    def __init__(self, user):
        self.service_instance = None
        self.endpoints = None
        super().__init__(user)

    def initialize(self, service_instance=None, service_vms=None, usecase_id=None):
        print('Initialized %s with service instance %s and service vms %s'%(
            self.__usecase__, service_instance, service_vms))
        self.service_instance = service_instance
        self.service_vms = service_vms
        super().initialize(usecase_id)

    def create(self, service_instance, service_vms, user=None):
        self.service_instance = service_instance
        self.service_vms = service_vms
        self.validate()
        super().create(user)

    def delete(self):
        self.service_instance = None
        self.service_vms = None
        self.validate()
        super().delete()

    def validate(self):
        pass

    def dump(self):
        return {"service_instance": self.service_instance, "service_vms": self.service_vms}
