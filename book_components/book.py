import json
from book_components.base_component import BaseComponent
from chatgpt_wrapper import ChatGPTWrapper


# Book class
class Book(BaseComponent):
    TEMPLATE_SUMMARY = f"Summarize this book. Limit the summary to {{max_tokens}} tokens. If you find the book's name or the authors' name, include it in the summary. Content: {{content}}."
    TEMPLATE_FIND_PAGE = f'This is a summary of a book snippet. Find the best sub-section or page to answer this question: "{{question}}". Answer the page or sub-section number in digits only. Answer "Not sure" if you are not sure. Summary: {{content}}. Limit the answer to {{max_tokens}} tokens.'
    TEMPLATE_ANSWER_WITH_SECTION = f'Answer the question with the content. Keep the answer short and concise. Content: "{{content}}" Question: {{question}}. Limit the answer to {{max_tokens}} tokens.'
    TEMPLATE_INTRO = "This is a book. Give yourself a proper name and introduce yourself with a breif summary. Please also provide three questions a reader may want to ask you. The format is 'You may want to ask me these questions...<bullet points>'. Book content: {content}"
    TEMPLATE_GET_NAME = 'Find the name of the book and the authors. Make the output ONLY in the format of a valid json array without explanation  {"book_name": "<book_name>", author_name: ["<author_name_1>", "<author_name_2>"]} Content: {content}'

    def __init__(self, name, authors, subcomponents):
        self.name = name
        self.authors = authors
        self.subcomponents = subcomponents
        self.hash = self.combine_hashes(
            self.compute_hash(self.name), self.compute_hash(','.join(self.authors)), self.hash
        )

    def get_summary(self):
        summary = f"{self.name} by {', '.join(self.authors)}\n\n" + super().get_summary()
        return summary

    def get_hash(self):
        return self.hash

    def get_intro(self):
        return ChatGPTWrapper.ask(
            self.TEMPLATE_INTRO.format(content=self.get_summary())
        )

    def get_book_and_author_names(self, content):
        prompt = self.TEMPLATE_GET_NAME.format(content=content)
        response = ChatGPTWrapper.ask(prompt=prompt)
        
        try:
            names = json.loads(response)
        except json.JSONDecodeError:
            names = {
                "book_name": "Unknown",
                "author_name": ["Unknown"]
            }
        return names["book_name"], names["author_name"]


    def update_book_and_author_names(self, book_name, authors):
        self.__init__(book_name, authors, self.subcomponents)
