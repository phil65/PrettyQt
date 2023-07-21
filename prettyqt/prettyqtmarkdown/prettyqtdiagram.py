from __future__ import annotations

import logging

from mknodes import connectionbuilder

from prettyqt import constants, core


logger = logging.getLogger(__name__)


class IndexConnectionBuilder(connectionbuilder.ConnectionBuilder):
    def __init__(self, index: core.ModelIindex, attribute_roles=None):
        super().__init__([index])
        self.attribute_roles = attribute_roles or []

    def get_id(self, item: core.ModelIndex) -> int:
        return id(item)

    def get_title(self, item: core.ModelIindex) -> str:
        return item.data(constants.DISPLAY_ROLE)

    def get_attributes(self, item: core.ModelIindex) -> list[str]:
        return [item.data(role) for role in self.attribute_roles]

    def get_children(self, item: core.ModelIindex) -> list[core.ModelIndex]:
        model = item.model()
        return [model.index(i, 0, item) for i in range(model.rowCount(item))]


class PrettyQtDiagram:
    pass
