from qtpy import QtHelp

from prettyqt import core


class HelpContentItem(QtHelp.QHelpContentItem):
    def __len__(self):
        return self.childCount()

    def get_url(self) -> core.Url:
        return core.Url(self.url())
