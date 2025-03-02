from __future__ import annotations

from typing import TYPE_CHECKING
import webbrowser

from prettyqt import core, webenginecore, widgets
from prettyqt.qt import QtWebEngineWidgets
from prettyqt.utils import datatypes


if TYPE_CHECKING:
    from collections.abc import Callable


# os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = "--enable-logging --log-level=3"


class WebEngineView(widgets.WidgetMixin, QtWebEngineWidgets.QWebEngineView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setPage(webenginecore.WebEnginePage(self))

    def set_url(self, url: datatypes.UrlType | datatypes.PathType):
        """Set the url of the WebEngineView.

        Clears the view and loads the URL.

        Args:
            url: URL to set
        """
        url = datatypes.to_url(url)
        self.setUrl(url)

    def get_url(self) -> core.Url:
        return core.Url(self.url())

    def load_url(self, url: datatypes.UrlType | datatypes.PathType):
        """Load the URL.

        Loads the specified url and displays it.

        Note: The view remains the same until enough data has arrived
        to display the new URL.

        Args:
            url: URL to load
        """
        url = datatypes.to_url(url)
        self.load(url)

    def set_zoom(self, zoom: float):
        """Set the zoom factor for the view.

        Valid values are within the range from 0.25 to 5.0. The default factor is 1.0.

        Args:
            zoom: Zoom factor
        """
        self.setZoomFactor(zoom)

    def find_text(
        self,
        string: str,
        backward: bool = False,
        case_sensitive: bool = False,
        callback: Callable[[bool], None] | None = None,
    ):
        """Find text in the current page.

        Finds the specified string, subString, in the page, using the given options.
        The findTextFinished() signal is emitted when a string search is completed.

        To clear the search highlight, just pass an empty string.

        The resultCallback must take a boolean parameter.
        It will be called with a value of true if the subString was found;
        otherwise the callback value will be false.

        Warning: It is guaranteed that the callback is always called,
        but it might be done during page destruction. When WebEnginePage is deleted,
        the callback is triggered with an invalid value and it is not safe to use
        the corresponding QWebEnginePage or QWebEngineView instance inside it.

        Args:
            string: string to search for
            backward: search backwards
            case_sensitive: case-sensitive search
            callback: result callback
        """
        if callback is None:

            def do_nothing(x):
                pass

            callback = do_nothing
        flag = webenginecore.WebEnginePage.FindFlag(0)
        if case_sensitive:
            flag |= webenginecore.WebEnginePage.FindFlag.FindCaseSensitively
        if backward:
            flag |= webenginecore.WebEnginePage.FindFlag.FindBackward
        self.findText(string, flag, callback)

    def get_settings(self) -> webenginecore.WebEngineSettings:
        settings = self.settings()
        return webenginecore.WebEngineSettings(settings)

    def set_setting(
        self,
        setting_name: webenginecore.webenginesettings.WebAttributeStr,
        value: bool,
    ):
        self.get_settings()[setting_name] = value

    def get_setting(
        self, setting_name: webenginecore.webenginesettings.WebAttributeStr
    ) -> bool:
        return self.get_settings()[setting_name]

    @classmethod
    def register_as_browser(cls, tabwidget: widgets.TabWidget):
        class BuiltInBrowser(webbrowser.BaseBrowser):
            def open(self, url: str, new: int = 0, autoraise: bool = True):
                # logger.info(f"opening {url} with builtin browser..")
                webview = cls()
                webview.load_url(url)
                if new == 1:
                    webview.show()
                else:
                    tabwidget.add_tab(webview, url, show=autoraise)

        webbrowser.register("BuiltInBrowser", BuiltInBrowser)

    def last_context_menu_request(
        self,
    ) -> webenginecore.WebEngineContextMenuRequest | None:
        req = self.lastContextMenuRequest()
        return webenginecore.WebEngineContextMenuRequest(req) if req else None


if __name__ == "__main__":
    import pathlib

    from prettyqt import widgets

    app = widgets.app()
    widget = WebEngineView()

    import markdown

    path = pathlib.Path("E:\\dev\\prettyqt\\docs\\index.md")

    extensions = [
        "pymdownx.arithmatex",
        "pymdownx.betterem",
        "pymdownx.caret",
        "pymdownx.critic",
        "pymdownx.details",
        "pymdownx.emoji",
        "pymdownx.inlinehilite",
        "pymdownx.magiclink",
        "pymdownx.mark",
        "pymdownx.smartsymbols",
        "pymdownx.superfences",
        "pymdownx.tasklist",
        "pymdownx.tabbed",
        "pymdownx.tilde",
    ]

    html = markdown.markdown(path.read_text(), extensions=extensions)
    widget.setHtml(html)
    page = widget.page()
    path = pathlib.Path(
        "E:\\dev\\prettyqt\\site\\assets\\stylesheets\\main.26e3688c.min.css"
    )
    page.insert_stylesheet("main.26e3688c.min", path)
    widget.show()
    app.exec()
