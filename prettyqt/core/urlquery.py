from __future__ import annotations

from collections.abc import MutableMapping
from typing import Any

from typing_extensions import Self

from prettyqt.qt import QtCore
from prettyqt.utils import datatypes, get_repr


class UrlQuery(QtCore.QUrlQuery, MutableMapping, metaclass=datatypes.QABCMeta):
    def __repr__(self):
        return get_repr(self, self.toString())

    def __str__(self):
        return self.toString()

    def __contains__(self, key: str):
        return self.hasQueryItem(key)

    def __add__(self, other: dict) -> Self:
        for k, v in other.items():
            self.addQueryItem(k, str(v))
        return self

    def __delitem__(self, item: str):
        self.removeQueryItem(item)

    def __setitem__(self, key, value):
        items = dict(self.queryItems())
        items[key] = value
        items = list(items.items())
        self.setQueryItems(items)

    def __len__(self):
        return len(self.queryItems())

    def __iter__(self):
        return iter(i[0] for i in self.queryItems())

    def __getitem__(self, key: str):
        return self.queryItemValue(key)

    def serialize(self) -> dict[str, Any]:
        return dict(path=self.toString())

    # def add_query_items(self, **items: str):
    #     for k, v in items.items():
    #         self.addQueryitem(k, v)


if __name__ == "__main__":
    query = UrlQuery()
    query["test"] = "hallo"
    query["test2"] = "hallo"
    query.pop("test")
    print(dict(query))
