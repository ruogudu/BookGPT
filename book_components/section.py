import re

from book_components.base_component import BaseComponent
from chatgpt_wrapper import ChatGPTWrapper
from config import SUMMARY_MAX_TOKENS


class Section(BaseComponent):
    TEMPLATE_SUMMARY = f"Summarize this section of a book. Limit the summary to {{max_tokens}} tokens. If you find the book's name or the authors' name, include it in the summary. Content: {{content}}."
    TEMPLATE_FIND_PAGE = f'This is a summary of a book snippet. Find the best section to answer this question: "{{question}}". Answer the section number in digits only. Answer "Not sure" if you are not sure. Summary: {{content}}. Limit the answer to {{max_tokens}} tokens.'
    TEMPLATE_ANSWER_WITH_SECTION = f'Answer the question with the content. Keep the answer short and concise. Content: "{{content}}" Question: {{question}}. Limit the answer to {{max_tokens}} tokens.'

    def __init__(self, id, subcomponents):
        super().__init__()
        self.id = id
        self.subcomponents = subcomponents
        self.content = self.curate_content(subcomponents)
        self.summary = self.curate_summary(id, self.content)
        self.hash = self.combine_hashes(
            self.compute_hash(str(self.id)),
            self.compute_hash(self.version),
            self.compute_hash(self.content),
            self.compute_hash(self.summary),
            *[subcomponent.get_hash() for subcomponent in self.subcomponents],
        )

    def ask_question(self, question):
        best_subcomponent = self.get_best_subcomponent(question)
        if best_subcomponent is None:
            return ChatGPTWrapper.ask(
                self.TEMPLATE_ANSWER_WITH_SECTION.format(
                    max_tokens=SUMMARY_MAX_TOKENS,
                    content=self.content,
                    question=question,
                )
            )
        return self.subcomponents[best_subcomponent].ask_question(question)

    def get_summary(self):
        return self.summary

    def get_hash(self):
        return self.hash

    def get_id(self):
        return self.id

    def get_best_subcomponent(self, question):
        prompt = self.TEMPLATE_FIND_PAGE.format(
            max_tokens=SUMMARY_MAX_TOKENS,
            content=self.content,
            question=question,
        )
        answer = ChatGPTWrapper.ask(prompt=prompt)
        subcomponent_id = re.search(r"\d+", answer)
        if subcomponent_id is None:
            return None
        return int(subcomponent_id.group())

    @staticmethod
    def curate_summary(id, content):
        prompt = Section.TEMPLATE_SUMMARY.format(
            max_tokens=SUMMARY_MAX_TOKENS, content=content
        )
        answer = ChatGPTWrapper.ask(
            prompt=prompt,
            max_tokens=SUMMARY_MAX_TOKENS,
        )
        return "Section {id}: {summary}".format(id=id, summary=answer)

    @staticmethod
    def curate_content(subcomponents):
        content = ""
        for subcomponent in subcomponents:
            content += subcomponent.get_summary() + "\n\n"
        return content
