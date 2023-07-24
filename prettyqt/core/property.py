from __future__ import annotations

from prettyqt.qt import QtCore


class Property(QtCore.Property):
    """Template class that enables automatic property bindings."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.doc = kwargs.get("doc")

    @classmethod
    def get_doc_dict(cls, klass: type):
        import inspect

        result = {}
        for name, member in inspect.getmembers(klass):
            if isinstance(member, cls):
                result[name] = member.doc
        return result


if __name__ == "__main__":
    prop = Property(int)
