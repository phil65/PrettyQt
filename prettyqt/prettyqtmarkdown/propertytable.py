from __future__ import annotations

import logging

import mknodes

from prettyqt import core


logger = logging.getLogger(__name__)


class PropertyTable(mknodes.MkTable):
    def __init__(
        self,
        qobject: core.QObject | type[core.QObject],
        user_prop_name: str | None = None,
        header: str = "",
    ):
        lines = []
        headers = ["Qt Property", "Type", "Options"]
        if isinstance(qobject, core.QObject):
            properties = core.MetaObject(qobject.metaObject()).get_properties()
        elif issubclass(qobject, core.QObject):
            properties = core.MetaObject(qobject.staticMetaObject).get_properties()
        for prop in properties:
            property_name = f"`{prop.get_name()}`"
            if prop.get_name() == user_prop_name:
                property_name += " *(User property)*"
            # if (flag := prop.get_enumerator()):
            meta_type = prop.get_meta_type()
            label = (meta_type.get_name() or "").rstrip("*")
            mark = "x" if prop.get_name() == user_prop_name else ""
            sections = [property_name, f"**{label}**", mark]
            lines.append(sections)
        super().__init__(columns=headers, data=list(zip(*lines)), header=header)


if __name__ == "__main__":
    table = PropertyTable(core.StringListModel)
    print(table.to_markdown())
