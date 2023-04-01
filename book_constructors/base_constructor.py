"""Base class for all book constructors"""
from abc import ABC, abstractmethod


class BaseConstructor(ABC):
    @abstractmethod
    def construct_book(self):
        # Construct the book
        pass

    @abstractmethod
    def resume_book(self, book_to_resume):
        pass
