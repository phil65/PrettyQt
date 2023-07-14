from __future__ import annotations

from collections.abc import Callable, Mapping, Sequence
import importlib
import inspect
import logging

from typing_extensions import Self

from prettyqt.utils import markdownizer


logger = logging.getLogger(__name__)


class Table(markdownizer.BaseSection):
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

    @classmethod
    def for_items(cls, items, columns: dict[str, Callable]):
        ls = [{k: v(item) for k, v in columns.items()} for item in items]
        return cls(ls)

    # class ClassTable(Table):

    @classmethod
    def get_classes_table(
        cls,
        klasses: list[type],
        filter_fn: Callable | None = None,
        shorten_lists_after: int = 10,
    ) -> Self:
        """Create a table containing information about a list of classes.

        Includes columns for child and parent classes including links.
        """
        ls = []
        if filter_fn is None:

            def always_true(_):
                return True

            filter_fn = always_true
        for kls in klasses:
            subclasses = [subkls for subkls in kls.__subclasses__() if filter_fn(subkls)]
            subclass_links = [markdownizer.link_for_class(sub) for sub in subclasses]
            subclass_str = markdownizer.to_html_list(
                subclass_links, shorten_after=shorten_lists_after
            )
            parents = kls.__bases__
            parent_links = [markdownizer.link_for_class(parent) for parent in parents]
            parent_str = markdownizer.to_html_list(
                parent_links, shorten_after=shorten_lists_after
            )
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
    def get_module_overview(
        cls, module: str | None = None, predicate: Callable | None = None
    ):
        mod = importlib.import_module(module)
        rows = [
            (
                submod_name,
                # markdownizer.link_for_class(submod, size=4, bold=True),
                (
                    submod.__doc__.split("\n")[0]
                    if submod.__doc__
                    else "*No docstrings defined.*"
                ),
                (
                    markdownizer.to_html_list(submod.__all__, make_link=True)
                    if hasattr(submod, "__all__")
                    else ""
                ),
            )
            for submod_name, submod in inspect.getmembers(mod, inspect.ismodule)
            if (predicate is None or predicate(submod)) and "__" not in submod.__name__
        ]
        rows = list(zip(*rows))
        return cls(rows, columns=["Name", "Information", "Members"])

    @classmethod
    def get_ancestor_table_for_klass(cls, klass: type) -> Self | None:
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


if __name__ == "__main__":
    table = Table()
    print(logger.warning(table))
