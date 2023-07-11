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


if __name__ == "__main__":
    section = BaseSection(module_name="prettyqt")
    section.to_markdown()
