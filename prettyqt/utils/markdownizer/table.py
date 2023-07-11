from __future__ import annotations

from collections.abc import Callable, Mapping, Sequence

from prettyqt import core
from prettyqt.utils import markdownizer


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
                self.data = {h[i]: col for i, col in enumerate(data)}
            case (dict(), *_):
                self.data = v = {k: [dic[k] for dic in data] for k in data[0]}
        for k, v in column_modifiers.items():
            self.data[k] = [v(i) for i in self.data[k]]

    @classmethod
    def get_property_table(
        cls, props, user_prop_name: str | None = None, header: str = ""
    ) -> Table:
        lines = []
        headers = ["Qt Property", "Type", "User property"]
        for prop in props:
            sections: list[str] = [
                f"`{prop.get_name()}`",
                f"**{(prop.get_meta_type().get_name() or '').rstrip('*')}**",
                "x" if prop.get_name() == user_prop_name else "",
            ]
            lines.append(sections)
        return cls(columns=headers, data=list(zip(*lines)), header=header)

    @classmethod
    def get_prop_tables_for_klass(cls, klass: type[core.QObject]) -> list[Table]:
        metaobject = core.MetaObject(klass.staticMetaObject)
        user_prop_name = (
            user_prop.get_name()
            if (user_prop := metaobject.get_user_property()) is not None
            else None
        )
        props_without_super = metaobject.get_properties(include_super=False)
        prop_names_without_super = [p.get_name() for p in props_without_super]
        props_with_super = metaobject.get_properties(include_super=True)
        super_props = [
            p for p in props_with_super if p.get_name() not in prop_names_without_super
        ]
        if not props_with_super:
            return []
        lines = []
        if props_without_super:
            item = cls.get_property_table(
                props_without_super, user_prop_name, header="Class Properties"
            )
            lines.append(item)
        if super_props:
            item = cls.get_property_table(
                super_props, user_prop_name, header="Inherited Properties"
            )
            lines.append(item)
        return lines

    @classmethod
    def get_classes_table(
        cls,
        klasses: list[type],
        filter_fn: Callable | None = None,
    ) -> Table:
        """Create a table containing information about a list of classes.

        Includes columns for child and parent classes including links.
        """
        ls = []
        if filter_fn is None:

            def filter_fn(_):
                return True

        for kls in klasses:
            subclasses = [subkls for subkls in kls.__subclasses__() if filter_fn(subkls)]
            parents = kls.__bases__
            subclass_str = ", ".join(
                markdownizer.link_for_class(sub) for sub in subclasses
            )
            parent_str = ", ".join(
                markdownizer.link_for_class(parent) for parent in parents
            )
            desc = [
                kls.__doc__.split("\n")[0] if kls.__doc__ else "" for kls in subclasses
            ]
            data = dict(
                Name=markdownizer.link_for_class(kls),
                # Module=kls.__module__,
                Children=subclass_str,
                Inherits=parent_str,
                Description=desc,
            )
            ls.append(data)
        return cls(ls)

    @classmethod
    def get_dependency_table(cls, distribution):
        from prettyqt import itemmodels

        model = itemmodels.ImportlibTreeModel("prettyqt")
        list(model.iter_tree(depth=2))
        proxy = itemmodels.ColumnOrderProxyModel(
            order=["Name", "Constraints", "Extra", "Summary", "Homepage"],
            source_model=model,
        )
        return cls.from_itemmodel(proxy)

    @classmethod
    def get_ancestor_table_for_klass(cls, klass: type[core.QObject]) -> Table | None:
        subclasses = klass.__subclasses__()
        if not subclasses:
            return None
        # STRIP_CODE = r"```[^\S\r\n]*[a-z]*\n.*?\n```"
        # docs = [re.sub(STRIP_CODE, '', k.__module__, 0, re.DOTALL) for k in subclasses]
        desc = [kls.__doc__.split("\n")[0] if kls.__doc__ else "" for kls in subclasses]
        data = dict(
            Class=[markdownizer.link_for_class(kls) for kls in subclasses],
            Module=[kls.__module__ for kls in subclasses],
            Description=desc,
        )
        return cls(data=data, header="Child classes")

    @classmethod
    def from_itemmodel(
        cls,
        model: core.AbstractItemModelMixin,
        use_checkstate_role: bool = True,
        **kwargs,
    ) -> Table:
        from prettyqt import constants

        data, h_header, _ = model.get_table_data(**kwargs)
        if use_checkstate_role:
            kwargs["role"] = constants.CHECKSTATE_ROLE
            check_data, _, __ = model.get_table_data(**kwargs)
            for i, row in enumerate(data):
                for j, _column in enumerate(row):
                    if check_data[i][j]:
                        data[i][j] = "x"
        data = list(zip(*data))
        return cls(data, columns=h_header)

    def _to_markdown(self) -> str:
        # print(self.data)
        headers = [str(i) for i in self.data.keys()]
        lines = [f"|{'|'.join(headers)}|", f"|{'--|--'.join('' for _ in headers)}|"]
        lines.extend(f"|{'|'.join(row)}|" for row in self._iter_rows())
        return "\n".join(lines)

    def _iter_rows(self):
        length = min(len(i) for i in self.data.values())
        for j, _ in enumerate(range(length)):
            yield [self.data[k][j] or "" for k in self.data.keys()]
