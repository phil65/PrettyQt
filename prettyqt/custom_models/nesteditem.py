from __future__ import annotations

from collections.abc import Iterable


class NestedItem:

    item_name = "not_defined"

    def __init__(
        self,
        parent: NestedItem | None = None,
        dynamic_name: str | None = None,
        count: int | None = None,
        children: list[NestedItem] | None = None,
    ):
        self.parent = parent
        self.dynamic_name = dynamic_name if dynamic_name else self.item_name
        self.count = count
        # self.timestamp = kwargs.pop("timestamp", time.time())
        self.children: list[NestedItem] = list()
        if children:
            self.add_children(children)

    def __iter__(self):
        return iter(self.children)

    def add_children(self, children: Iterable):
        for child in children:
            child.parent = self
        self.children.extend(children)

    def append_child(self, item):
        self.children.append(item)

    def child(self, row: int) -> NestedItem:
        return self.children[row]

    def row(self) -> int:
        """Return row number.

        returns row position of item inside parent´s children
        returns 0 if no parent available

        Returns:
            row number
        """
        return self.parent.children.index(self) if self.parent else 0

    def iter_tree(
        self,
        name: str | None = None,
        yield_self: bool = True,
        recursive: bool = True,
        level: int = 0,
        count: int = 0,
        assign_names: bool = True,
    ):
        """Yield children from bottom to top, yield self at end.

        assigns dynamic vars count, level and dynamic name
        """
        if name is None:
            name = self.item_name
        for i, c in enumerate(self.children, start=1):
            count += 1
            level += 1
            with_suffix = f"{name}_{i}" if len(self.children) > 1 else name
            if recursive:
                yield from c.iter_tree(
                    with_suffix, yield_self=False, level=level, count=count
                )
            if assign_names:
                c.dynamic_name, c.count = with_suffix, count
            yield c
            level -= 1
        if yield_self:
            if assign_names:
                self.dynamic_name, self.count = name, 0
            yield self
