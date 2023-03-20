import hashlib
from abc import ABC, abstractmethod

from config import VERSION


# Base class for all book components
class BaseComponent(ABC):
    def __init__(self):
        self.version = VERSION

    @abstractmethod
    def get_summary(self):
        # Get the summary of the component
        pass

    @abstractmethod
    def ask_question(self, question):
        # Ask a question about the component
        pass

    def get_id(self):
        # Get the id of the component
        return self.id

    @abstractmethod
    def get_hash(self):
        # Get the hash of the component
        pass

    @staticmethod
    def compute_hash(content):
        hash_object = hashlib.md5(content.encode())
        return hash_object.hexdigest()

    @staticmethod
    def combine_hashes(hashes):
        hash_object = hashlib.md5("".join(hashes).encode())
        return hash_object.hexdigest()
