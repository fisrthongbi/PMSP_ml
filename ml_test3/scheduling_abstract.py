from abc import *


class JobAbstract(metaclass=ABCMeta):
    @abstractmethod
    def getSetup(self, machine):
        pass


class MachineAbstract(metaclass=ABCMeta):
    @abstractmethod
    def process(self):
        pass


class InstanceAbstract(metaclass=ABCMeta):
    @abstractmethod
    def getPTime(self):
        pass

    @abstractmethod
    def getSetup(self):
        pass