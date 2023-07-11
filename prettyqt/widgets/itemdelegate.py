from __future__ import annotations

from prettyqt import widgets


class ItemDelegate(widgets.AbstractItemDelegateMixin, widgets.QItemDelegate):
    """Display and editing facilities for data items from a model."""
