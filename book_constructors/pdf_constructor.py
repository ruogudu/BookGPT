"""Construct a book from a PDF file."""
from book_components.book import Book
from book_components.section import Section
from book_components.page import Page
from book_constructors.base_constructor import BaseConstructor
from pdf_wrapper import PDFWrapper


PAGE_COUNT_PER_SECTION = 10


class PDFConstructor(BaseConstructor):
    def __init__(self, book_title, book_author, pdf_wrapper: PDFWrapper):
        self.pdf_wrapper = pdf_wrapper
        self.book_title = book_title
        self.book_author = book_author

    def construct_book(self):
        num_pages = self.pdf_wrapper.get_num_pages()
        sections = []

        for section_start in range(0, num_pages, PAGE_COUNT_PER_SECTION):
            section_end = min(section_start + PAGE_COUNT_PER_SECTION, num_pages)
            pages = [
                Page(page_num, self.pdf_wrapper.get_page(page_num))
                for page_num in range(section_start, section_end)
            ]
            sections.append(Section(len(sections) + 1, pages))

        # Replace the placeholders with actual title and author information.
        title = self.book_title
        author = self.book_author
        return Book(title, author, sections)

    def resume_book(self, book_to_resume):
        pass
