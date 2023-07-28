from __future__ import annotations

import logging

import mknodes

from prettyqt import core


logger = logging.getLogger(__name__)


class MkPropertyTable(mknodes.MkTable):
    """A table containing info about Qt properties."""

    def __init__(
        self,
        qobject: type[core.QObject],
        user_prop_name: str | None = None,
        header: str = "",
    ):
        lines = []
        headers = ["Qt Property", "Type", "Doc"]
        properties = core.MetaObject(qobject.staticMetaObject).get_properties()
        doc_dict = core.Property.get_doc_dict(qobject)
        for prop in properties:
            property_name = f"`{prop.get_name()}`"
            if prop.get_name() == user_prop_name:
                property_name += " *(User property)*"
            # if (flag := prop.get_enumerator()):
            meta_type = prop.get_meta_type()
            label = (meta_type.get_name() or "").rstrip("*")
            doc = doc_dict.get(prop.get_name(), "")
            # mark = "x" if prop.get_name() == user_prop_name else ""
            sections = [property_name, f"**{label}**", doc]
            lines.append(sections)
        super().__init__(columns=headers, data=list(zip(*lines)), header=header)


if __name__ == "__main__":
    table = MkPropertyTable(core.StringListModel)
    dct = core.Property.get_doc_dict(core.StringListModel)
    print(dct)
    # print(table.to_markdown())
