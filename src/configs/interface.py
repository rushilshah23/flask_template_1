from abc import ABC, abstractmethod



class IConfig(ABC):
    pass



class IConfig_Factory(ABC):
    @abstractmethod
    def get_config(self)->IConfig:
        pass



