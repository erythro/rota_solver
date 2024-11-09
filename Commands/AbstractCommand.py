from abc import ABC, abstractmethod
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
    def execute(self, args):
        pass