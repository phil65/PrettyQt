from prettyqt import widgets
from prettyqt.qt import QtCore, QtHelp
from prettyqt.utils import datatypes


class HelpContentWidget(widgets.TreeViewMixin, QtHelp.QHelpContentWidget):
    """Tree view for displaying help content model items."""

    def index_of(self, url: datatypes.UrlType) -> QtCore.QModelIndex | None:
        idx = self.indexOf(datatypes.to_url(url))
        return idx if idx.isValid() else None

    @classmethod
    def setup_example(cls):
        return None
