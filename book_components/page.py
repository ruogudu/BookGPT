import hashlib

from book_components.base_component import BaseComponent
from chatgpt_wrapper import ChatGPTWrapper
from config import SUMMARY_MAX_TOKENS


class Page(BaseComponent):
    TEMPLATE_SUMMARY = "Summarize this page of a book. {content}"
    TEMPLATE_ANSWER_WITH_PAGE = 'Answer the question with the content. Keep the answer short and concise. Context: "{content}" Question: {question}'

    def __init__(self, id, content):
        super().__init__()
        self.id = id
        self.content = content
        self.summary = self.curate_summary(id, content)
        self.hash = self.combine_hashes(
            self.compute_hash(str(self.id)),
            self.compute_hash(self.version),
            self.compute_hash(self.content),
            self.compute_hash(self.summary),
        )

    def ask_question(self, question):
        prompt = self.TEMPLATE_ANSWER_WITH_PAGE.format(
            question=question,
            content=self.content,
        )
        answer = ChatGPTWrapper.ask(prompt=prompt)
        answer += f" (Page {self.id})"
        return answer

    def get_summary(self):
        return self.summary

    def get_hash(self):
        return self.hash

    def get_id(self):
        return self.id

    @staticmethod
    def curate_summary(id, content):
        prompt = Page.TEMPLATE_SUMMARY.format(content=content)
        answer = ChatGPTWrapper.ask(
            prompt=prompt,
            max_tokens=SUMMARY_MAX_TOKENS,
        )
        return "Page {id}: {summary}".format(id=id, summary=answer)
