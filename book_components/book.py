import json
from book_components.base_section import BaseSection
from chatgpt_wrapper import ChatGPTWrapper
from config import SUMMARY_MAX_TOKENS


# Book class
class Book(BaseSection):
    TEMPLATE_SUMMARY = "Summarize this book. Limit the summary to {max_tokens} tokens. If you find the book's name or the authors' name, include it in the summary. Content: {content}."
    TEMPLATE_INTRO = "Act as this book itself. Give yourself a proper name and introduce yourself with a breif summary. Please also provide three questions a reader may want to ask you. The format is 'You may want to ask me these questions...<bullet points>'. Book content: {content}"
    TEMPLATE_GET_NAME = 'Find the name of the book and the authors. Make the output ONLY in the format of a valid json object without explanation, format: {{"book_name": "<book_name>", "author_name": ["<author_name_1>", "<author_name_2>"]}} Content: {content}'

    def __init__(self, name, authors, subcomponents):
        self.name = name
        self.authors = authors
        self.subcomponents = subcomponents
        self.content = self.curate_content(subcomponents)
        self.summary = self.curate_summary(self.content)
        self.hash = self.calc_hash()

    def calc_hash(self):
        return self.combine_hashes(
            self.compute_hash(self.name),
            self.compute_hash(",".join(self.authors)),
            self.compute_hash(self.summary),
            *[subcomponent.get_hash() for subcomponent in self.subcomponents],
        )

    def get_summary(self):
        summary = f"{self.name} by {', '.join(self.authors)}\n\n" + self.summary
        return summary

    def get_content(self):
        content = f"{self.name} by {', '.join(self.authors)}\n\n" + self.content
        return content

    def get_intro(self):
        return ChatGPTWrapper.ask(self.TEMPLATE_INTRO.format(content=self.content))

    def get_book_and_author_names(self):
        prompt = self.TEMPLATE_GET_NAME.format(content=self.content)
        response = ChatGPTWrapper.ask(prompt=prompt)

        try:
            names = json.loads(response)
        except json.JSONDecodeError:
            names = {"book_name": "Unknown", "author_name": ["Unknown"]}
        if not isinstance(names, dict):
            names = {"book_name": "Unknown", "author_name": ["Unknown"]}
        if "book_name" not in names:
            names["book_name"] = "Unknown"
        if "author_name" not in names:
            names["author_name"] = ["Unknown"]
        return names["book_name"], names["author_name"]

    def update_book_and_author_names(self, book_name, authors):
        self.name = book_name
        self.authors = authors
        self.hash = self.calc_hash()

    @staticmethod
    def curate_summary(content):
        prompt = Book.TEMPLATE_SUMMARY.format(
            max_tokens=SUMMARY_MAX_TOKENS, content=content
        )
        answer = ChatGPTWrapper.ask(
            prompt=prompt,
            max_tokens=SUMMARY_MAX_TOKENS,
        )
        return "Book summary: {summary}".format(summary=answer)
