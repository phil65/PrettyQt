from qtpy import QtHelp

from prettyqt import core


class HelpLink(QtHelp.QHelpLink):
    def get_url(self) -> core.Url:
        return core.Url(self.url)
