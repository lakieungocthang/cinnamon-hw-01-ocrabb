from abc import ABC, abstractmethod

class CustomHandler(ABC):
    @abstractmethod
    def process(self, file):
        pass

    @abstractmethod
    def save_to_local(self, data):
        pass

    @abstractmethod
    def save_to_cloud(self, data):
        pass
