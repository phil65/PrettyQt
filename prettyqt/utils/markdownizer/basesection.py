from __future__ import annotations

import logging

import mkdocs_gen_files

from prettyqt.utils import get_repr, node


logger = logging.getLogger(__name__)


class BaseSection(node.BaseNode):
    """Base class for everything which can be expressed as Markup.

    The class inherits from BaseNode. The idea is that starting from the
    root nav (aka Docs) down to nested Markup blocks, the whole project can be represented
    by one tree.
    """

    def __init__(self, header: str = ""):
        super().__init__()
        self.header = header

    def __str__(self):
        return self.to_markdown()

    def to_markdown(self):
        text = self._to_markdown() + "\n"
        return f"## {self.header}\n\n{text}" if self.header else text

    def virtual_files(self):
        return {}

    def all_virtual_files(self):
        """Return a dictionary containing all virtual files of itself and all children."""
        dct = {k: v for des in self.descendants for k, v in des.virtual_files().items()}
        return dct | self.virtual_files()

    def write(self):
        # path = pathlib.Path(self.path)
        # path.parent.mkdir(parents=True, exist_ok=True)
        for k, v in self.all_virtual_files().items():
            logger.info(f"Written file to {k}")
            mode = "w" if isinstance(v, str) else "wb"
            with mkdocs_gen_files.open(k, mode) as file:
                file.write(v)


class Text(BaseSection):
    """Class for any Markup text.

    All classes inheriting from BaseSection can get converted to this Type.
    """

    def __init__(self, text: str | BaseSection = "", header: str = ""):
        super().__init__(header=header)
        self.text = text

    def __repr__(self):
        return get_repr(self, text=self.text)

    def _to_markdown(self) -> str:
        return self.text if isinstance(self.text, str) else self.text.to_markdown()


class Code(Text):
    """Class representing a Code block."""

    def __init__(
        self,
        language: str,
        text: str | BaseSection = "",
        header: str = "",
        linenums: int | None = None,
        hl_lines: list[int] | None = None,
        title: str = "",
    ):
        super().__init__(text, header)
        self.language = language
        self.title = title
        self.linenums = linenums

    def _to_markdown(self) -> str:
        title = f" title={self.title}" if self.title else ""
        return f"```{self.language}{title}\n{self.text}\n```"


if __name__ == "__main__":
    section = BaseSection(module_name="prettyqt")
    section.to_markdown()
