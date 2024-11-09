from abc import ABC, abstractmethod
from Model.ModelFactory import Model
import argparse


class AbstractCommand(ABC):
    @abstractmethod
    def getName(self) -> str:
        pass
    @abstractmethod
    def getDesc(self) -> str:
        pass
    @abstractmethod
    def configure(self, parser):
        pass
    @abstractmethod
    def execute(self, argparse):
        pass