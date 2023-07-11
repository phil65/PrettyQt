from __future__ import annotations

import logging

from prettyqt.utils import markdownizer


logger = logging.getLogger(__name__)


class List(markdownizer.BaseSection):
    def __init__(self, listitems: list[str] | None = None, header: str = ""):
        super().__init__(header)
        self.listitems = listitems

    def __str__(self):
        return self.to_markdown()

    def _to_markdown(self):
        lines = [f"  - {i}" for i in self.listitems]
        return "\n" + "\n".join(lines) + "\n"


if __name__ == "__main__":
    section = List(["a", "b"], header="test")
    print(section.to_markdown())
