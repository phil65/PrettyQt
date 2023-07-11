from __future__ import annotations

import logging


logger = logging.getLogger(__name__)


class BaseSection:
    def __init__(self, header: str = ""):
        self.header = header

    def __str__(self):
        return self.to_markdown()

    def to_markdown(self):
        text = self._to_markdown() + "\n"
        if self.header:
            return f"## {self.header}\n\n{text}"
        return text


class Text(BaseSection):
    def __init__(self, text: str | BaseSection = "", header: str = ""):
        super().__init__(header=header)
        self.text = text

    def _to_markdown(self) -> str:
        return self.text if isinstance(self.text, str) else self.text.to_markdown()


class Code(Text):
    def __init__(self, language: str, text: str | BaseSection = "", header: str = ""):
        super().__init__(text, header)
        self.language = language

    def _to_markdown(self) -> str:
        return f"``` {self.language}\n{self.text}\n```"


if __name__ == "__main__":
    section = BaseSection(module_name="prettyqt")
    section.to_markdown()
