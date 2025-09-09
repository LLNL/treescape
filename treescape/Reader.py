from abc import ABC, abstractmethod

class Reader(ABC):
    @abstractmethod
    def get_entire(self, xaxis_name):
        pass

