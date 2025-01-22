from abc import ABC, abstractmethod

class AccessManager(ABC):
    @abstractmethod
    def add_data(self, *args, **kwargs): ...
    
    @abstractmethod
    def get_data(self, *args, **kwargs): ...
