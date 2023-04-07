"""Construct a book from a PDF file."""
import questionary
from alive_progress import alive_bar

from book_components.book import Book
from book_components.section import Section
from book_components.page import Page
from book_constructors.base_constructor import BaseConstructor
from pdf_wrapper import PDFWrapper


PAGE_COUNT_PER_SECTION = 10
SECTION_COUNT_PER_SECTION = 10


class PDFConstructor(BaseConstructor):
    def __init__(self, pdf_wrapper: PDFWrapper):
        self.pdf_wrapper = pdf_wrapper

    def construct_book(self):
        num_pages = self.pdf_wrapper.get_num_pages()
        sections = []

        with alive_bar(num_pages, length=40, spinner="dots_waves") as bar:
            for section_start in range(0, num_pages, PAGE_COUNT_PER_SECTION):
                section_end = min(section_start + PAGE_COUNT_PER_SECTION, num_pages)
                pages = [
                    Page(page_num, self.pdf_wrapper.get_page(page_num))
                    for page_num in range(section_start, section_end)
                ]
                for _ in range(section_start, section_end):
                    bar()
                sections.append(Section(len(sections) + 1, pages))

        if len(sections) == 1:
            sections = sections[0].subcomponents

        while len(sections) > SECTION_COUNT_PER_SECTION:
            new_sections = []
            with alive_bar(len(sections), length=40, spinner="dots_waves") as bar:
                for section_start in range(0, len(sections), SECTION_COUNT_PER_SECTION):
                    section_end = min(section_start + PAGE_COUNT_PER_SECTION, len(sections))
                    sub_sections = sections[section_start: section_end]
                    new_sections.append(Section(len(new_sections) + 1, sub_sections))
                    for _ in range(section_start, section_end):
                        bar()
            sections = new_sections

        temp_book = Book("", [], sections)
        book_name, authors = temp_book.get_book_and_author_names()
        print("Book name:", book_name)
        print("Author name(s):", ", ".join(authors))
        correct = questionary.confirm("Is the book name and author name(s) correct?").ask()
        if not correct:
            book_name = questionary.text("Enter the book name:").ask()
            author_text = questionary.text("Enter the author name(s), separate by ,:").ask()
            authors = [author.strip() for author in author_text.split(",")]
        temp_book.update_book_and_author_names(book_name, authors)
        return temp_book

    def resume_book(self, book_to_resume):
        pass
