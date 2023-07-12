from __future__ import annotations

from collections.abc import Callable, Mapping, Sequence
from importlib import metadata
import logging

from typing_extensions import Self

from prettyqt import core
from prettyqt.utils import markdownizer


logger = logging.getLogger(__name__)


class Table(markdownizer.Text):
    def __init__(
        self,
        data: Sequence[Sequence[str]] | Sequence[dict] | dict[str, list] | None = None,
        columns: Sequence[str] | None = None,
        column_modifiers: dict[str, Callable[[str], str]] | None = None,
        header: str = "",
    ):
        super().__init__(header=header)
        column_modifiers = column_modifiers or {}
        match data:
            case Mapping():
                self.data = {str(k): [str(i) for i in v] for k, v in data.items()}
            case ((str(), *_), *_):
                h = columns or [str(i) for i in range(len(data))]
                self.data = {}
                for i, col in enumerate(data):
                    self.data[h[i]] = [str(j) for j in col]
            case (dict(), *_):
                self.data = {k: [dic[k] for dic in data] for k in data[0]}
            case ():
                self.data = {}
            case _:
                raise TypeError(data)
        for k, v in column_modifiers.items():
            self.data[k] = [v(i) for i in self.data[k]]

    def _to_markdown(self) -> str:
        if not self.data:
            return ""
        headers = [str(i) for i in self.data.keys()]
        lines = [f"|{'|'.join(headers)}|", f"|{'--|--'.join('' for _ in headers)}|"]
        lines.extend(f"|{'|'.join(row)}|" for row in self._iter_rows())
        return "\n".join(lines)

    def _iter_rows(self):
        length = min(len(i) for i in self.data.values())
        for j, _ in enumerate(range(length)):
            yield [self.data[k][j] or "" for k in self.data.keys()]

    # class ClassTable(Table):

    @classmethod
    def get_classes_table(
        cls,
        klasses: list[type],
        filter_fn: Callable | None = None,
    ) -> Self:
        """Create a table containing information about a list of classes.

        Includes columns for child and parent classes including links.
        """
        ls = []
        if filter_fn is None:

            def filter_fn(_):
                return True

        for kls in klasses:
            subclasses = [subkls for subkls in kls.__subclasses__() if filter_fn(subkls)]
            subclass_links = [markdownizer.link_for_class(sub) for sub in subclasses]
            subclass_str = markdownizer.to_html_list(subclass_links, shorten_after=10)
            parents = kls.__bases__
            parent_links = [markdownizer.link_for_class(parent) for parent in parents]
            parent_str = markdownizer.to_html_list(parent_links, shorten_after=10)
            desc = kls.__doc__.split("\n")[0] if isinstance(kls.__doc__, str) else ""
            desc = markdownizer.escaped(desc)
            name = markdownizer.link_for_class(kls, size=4, bold=True)
            module = markdownizer.styled(kls.__module__, size=1, recursive=True)
            data = dict(
                Name=f"{name}<br>{module}<br>{desc}",
                # Module=kls.__module__,
                Children=subclass_str,
                Inherits=parent_str,
                # Description=desc,
            )
            ls.append(data)
        return cls(ls)

    @classmethod
    def get_ancestor_table_for_klass(cls, klass: type[core.QObject]) -> Self | None:
        subclasses = klass.__subclasses__()
        if not subclasses:
            return None
        # STRIP_CODE = r"```[^\S\r\n]*[a-z]*\n.*?\n```"
        # docs = [re.sub(STRIP_CODE, '', k.__module__, 0, re.DOTALL) for k in subclasses]
        desc = [
            kls.__doc__.split("\n")[0] if isinstance(kls.__doc__, str) else ""
            for kls in subclasses
        ]
        data = dict(
            Class=[markdownizer.link_for_class(kls) for kls in subclasses],
            Module=[kls.__module__ for kls in subclasses],
            Description=desc,
        )
        return cls(data=data, header="Child classes")

    @classmethod
    def get_property_table(
        cls,
        qobject: core.QObject | type[core.QObject],
        user_prop_name: str | None = None,
        header: str = "",
    ) -> Self:
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
            property_type = f"**{(meta_type.get_name() or '').rstrip('*')}**"
            sections: list[str] = [
                property_name,
                property_type,
                "x" if prop.get_name() == user_prop_name else "",
            ]
            lines.append(sections)
        return cls(columns=headers, data=list(zip(*lines)), header=header)

    @classmethod
    def from_itemmodel(
        cls,
        model: core.AbstractItemModelMixin,
        use_checkstate_role: bool = True,
        **kwargs,
    ) -> Self:
        from prettyqt import itemmodels

        proxy = itemmodels.SliceToMarkdownProxyModel(None, source_model=model)

        data, h_header, _ = proxy.get_table_data(
            use_checkstate_role=use_checkstate_role, **kwargs
        )
        data = list(zip(*data))
        return cls(data, columns=h_header)

    @classmethod
    def get_dependency_table(
        cls,
        distribution: str | metadata.Distribution = "prettyqt",
    ) -> Self:
        from prettyqt import itemmodels

        model = itemmodels.ImportlibTreeModel(distribution)
        proxy = itemmodels.ColumnOrderProxyModel(
            order=["Name", "Constraints", "Extra", "Summary", "Homepage"],
            source_model=model,
        )
        return cls.from_itemmodel(proxy)


if __name__ == "__main__":
    from prettyqt import itemmodels

    model = itemmodels.QObjectPropertiesModel(core.PropertyAnimation())
    # print(proxy.get_table_data(use_checkstate_role=True))
    table = Table.from_itemmodel(model)
    # list(model.iter_tree(depth=2))
    table = Table.get_dependency_table("prettyqt")
    print(logger.warning(table))
