from abc import ABC, abstractmethod
from utils.FileType import FileType
class CustomHandler(ABC):
    def __init__(self, type: FileType):
        self.type = type

    @abstractmethod
    def process(self, file):
        pass

    def save_to_local(self, raw_data, output_data):
        pass

    def save_to_cloud(self, raw_data, output_data):
        pass
