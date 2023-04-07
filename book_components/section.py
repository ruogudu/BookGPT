from book_components.base_section import BaseSection
from chatgpt_wrapper import ChatGPTWrapper
from config import SUMMARY_MAX_TOKENS


class Section(BaseSection):
    TEMPLATE_SUMMARY = f"Summarize this section of a book. Limit the summary to {{max_tokens}} tokens. If you find the book's name or the authors' name, include it in the summary. Content: {{content}}."

    def __init__(self, id, subcomponents):
        super().__init__()
        self.id = id
        self.subcomponents = subcomponents
        self.content = self.curate_content(subcomponents)
        self.summary = self.curate_summary(id, self.content)
        self.hash = self.combine_hashes(
            self.compute_hash(str(self.id)),
            self.compute_hash(self.version),
            self.compute_hash(self.summary),
            *[subcomponent.get_hash() for subcomponent in self.subcomponents],
        )

    def get_summary(self):
        return self.summary

    def get_id(self):
        return self.id

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
