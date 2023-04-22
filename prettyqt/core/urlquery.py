from __future__ import annotations

from typing import Any

from prettyqt.qt import QtCore


class UrlQuery(QtCore.QUrlQuery):
    def __repr__(self):
        return f"{type(self).__name__}({self.toString()!r})"

    def __str__(self):
        return self.toString()

    def __contains__(self, key: str):
        return self.hasQueryItem(key)

    def __add__(self, other: dict) -> UrlQuery:
        for k, v in other.items():
            self.addQueryItem(k, str(v))
        return self

    def __setitem__(self, key, value):
        items = dict(self.queryItems())
        items[key] = value
        items = list(items.items())
        self.setQueryItems(items)

    def __getitem__(self, key: str):
        return self.queryItemValue(key)

    def serialize_fields(self) -> dict[str, Any]:
        return dict(path=self.toString())

    def serialize(self) -> dict[str, Any]:
        return self.serialize_fields()

    # def add_query_items(self, **items: str):
    #     for k, v in items.items():
    #         self.addQueryitem(k, v)
