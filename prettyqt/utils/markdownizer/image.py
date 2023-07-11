from __future__ import annotations

import logging
import pathlib

from prettyqt.utils import markdownizer


logger = logging.getLogger(__name__)


class Image(markdownizer.BaseSection):
    def __init__(
        self, path: str, caption: str, title: str = "Image title", header: str = ""
    ):
        super().__init__(header=header)
        self.title = title
        self.caption = caption
        # TODO: linkreplacer doesnt work yet with full path
        self.path = pathlib.Path(path).name  # this should not be needed.

    def _to_markdown(self) -> str:
        lines = ["<figure markdown>", f"  ![{self.title}]({self.path})"]
        if self.caption:
            lines.append(f"  <figcaption>{self.caption}</figcaption>")
        lines.append("</figure>")
        return "\n".join(lines)


class BinaryImage(Image):
    def __init__(
        self,
        data: bytes,
        path: str,
        caption: str = "",
        title: str = "Image title",
        header: str = "",
    ):
        super().__init__(path=path, header=header, caption=caption, title=title)
        self.data = data

    def _to_markdown(self) -> str:
        import mkdocs_gen_files

        path = pathlib.Path(self.path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with mkdocs_gen_files.open(self.path, "wb") as file:
            file.write(self.data)
        logger.info(f"Written image to {self.path}")
        return super()._to_markdown()
