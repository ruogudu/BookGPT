from book_components.section import Section
from chatgpt_wrapper import ChatGPTWrapper


# Book class
class Book(Section):
    TEMPLATE_INTRO = "This is a book. {cpntent} Give yourself a proper name and introduce yourself with a breif summary. Please also provide three questions a reader may want to ask you. The format is 'You may want to ask me these questions...<bullet points>'."

    def __init__(self, title, author, subcomponents):
        super().__init__(1, subcomponents)
        self.title = title
        self.author = author
        self.summary = f"{self.title} by {self.author}\n\n" + super().get_summary()
        self.hash = self.compute_hash(
            self.compute_hash(self.title),
            self.compute_hash(self.author),
            self.hash)

    def get_summary(self):
        return self.summary

    def get_hash(self):
        return self.hash

    def get_intro(self):
        return ChatGPTWrapper.ask(self.TEMPLATE_INTRO.format(content=self.get_summary()))
