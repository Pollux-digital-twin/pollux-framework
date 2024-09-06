from abc import ABC, abstractmethod


class DatabaseDriverAbstract(ABC):
    """Abstract class for Databse Driver."""

    def __init__(self):
        self.conn = None
        self.parameters = dict()

    def update_parameters(self, parameters):
        for key, value in parameters.items():
            self.parameters[key] = value

    @abstractmethod
    def connect(self):
        return

    @abstractmethod
    def disconnect(self):
        self.conn = None

    @abstractmethod
    def read_data(self):
        return

    @abstractmethod
    def write_data(self):
        return
