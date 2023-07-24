from __future__ import annotations

from prettyqt.qt import QtCore


class Property(QtCore.Property):
    """Template class that enables automatic property bindings."""

    def __init__(self, *args, **kwargs):
        self.doc = kwargs.get("doc")
        super().__init__(*args, **kwargs)

    @classmethod
    def get_doc_dict(cls, klass: type):
        import inspect

        return {
            name: member.doc
            for name, member in inspect.getmembers(klass)
            if isinstance(member, cls) and hasattr(member, "doc")
        }


if __name__ == "__main__":
    prop = Property(int)
