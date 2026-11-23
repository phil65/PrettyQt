from __future__ import annotations

import logging
from typing import Any

from mknodes.info import linkprovider


logger = logging.getLogger(__name__)


class QtLinkProvider(linkprovider.LinkProvider):
    def link_for_klass(self, kls: Any, from_page: Any = None) -> str:
        if isinstance(kls, type) and kls.__module__.startswith("prettyqt"):
            return linkprovider.linked(kls.__qualname__)
        # from_page was added in mknodes 3.1, only pass it on if given.
        kwargs = {} if from_page is None else {"from_page": from_page}
        return super().link_for_klass(kls, **kwargs)


if __name__ == "__main__":
    provider = QtLinkProvider()
