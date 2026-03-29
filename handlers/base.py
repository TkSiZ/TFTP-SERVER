from abc import ABC, abstractmethod


class TransferHandler(ABC):

    @abstractmethod
    def handle(self, session):
        pass