from __future__ import annotations

import logging

from mknodes.info import linkprovider


logger = logging.getLogger(__name__)


class QtLinkProvider(linkprovider.LinkProvider):
    def link_for_klass(self, kls: type):
        mod_path = kls.__module__
        if mod_path.startswith("prettyqt"):
            return linkprovider.linked(kls.__qualname__)
        return super().link_for_klass(kls)


if __name__ == "__main__":
    provider = QtLinkProvider()
