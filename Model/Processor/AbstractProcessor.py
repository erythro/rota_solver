from abc import ABC, abstractmethod
from Model.ModelFactory import Model

class AbstractProcessor(ABC):
    @abstractmethod
    def process(self, model: Model):
        pass