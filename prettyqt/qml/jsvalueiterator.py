from __future__ import annotations

from prettyqt.qt import QtQml


class JSValueIterator(QtQml.QJSValueIterator):
    """Java-style iterator for JSValue."""

    def __iter__(self):
        return self

    def __next__(self):
        if self.next():
            return (self.name(), self.value().toVariant())
        raise StopIteration
