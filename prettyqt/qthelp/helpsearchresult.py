from qtpy import QtHelp

from prettyqt import core


class HelpSearchResult(QtHelp.QHelpSearchResult):
    def get_url(self) -> core.Url:
        return core.Url(self.url)
