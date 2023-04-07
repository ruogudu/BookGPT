import re
from abc import ABC

from book_components.base_component import BaseComponent
from chatgpt_wrapper import ChatGPTWrapper
from config import SUMMARY_MAX_TOKENS


class BaseSection(BaseComponent, ABC):
    TEMPLATE_ANSWER_WITH_SECTION = f'Answer the question with the content. Keep the answer short and concise. Content: "{{content}}" Question: {{question}}. Limit the answer to {{max_tokens}} tokens.'
    TEMPLATE_FIND_PAGE = f'This is a summary of a book snippet. Find the best section or page to answer this question: "{{question}}". Answer the section/page number in digits only. Answer "Not sure" if you are not sure. Summary: {{content}}. Limit the answer to {{max_tokens}} tokens.'

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

    def get_hash(self):
        return self.hash

    @staticmethod
    def curate_content(subcomponents):
        content = ""
        for subcomponent in subcomponents:
            content += subcomponent.get_summary() + "\n\n"
        return content
