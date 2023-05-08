from __future__ import annotations

import logging
import re
import webbrowser

import requests

from prettyqt import core, widgets
from prettyqt.qt import QtCore


logger = logging.getLogger(__name__)

GITHUB_MESSAGE = (
    "You can download the new version for your operating system from GitHub.\n\n"
    "Do you want to visit the release website now?"
)

PYPI_MESSAGE = (
    "You should upgrade from command line with 'pip install prettyqt --upgrade'.\n\n"
    "Do you want to view the changelog on github?"
)


class WorkerSignals(core.Object):
    """TrayMenus' communication bus."""

    download_finished = QtCore.Signal(bytes, str)  # response, url
    download_failed = QtCore.Signal(str, str)  # msg, url


class Worker(QtCore.QRunnable):
    def __init__(self, url: str, timeout: int = 30) -> None:
        super().__init__()
        self.url = url
        self.timeout = timeout
        self.signals = WorkerSignals()

    @QtCore.Slot()
    def run(self) -> None:
        try:
            req = requests.get(self.url, verify=True, timeout=self.timeout)
        except Exception as e:
            msg = f"Exception '{e}' during download of '{self.url}'"
            logger.error(msg)
            self.signals.download_failed.emit(msg, self.url)
        else:
            self.signals.download_finished.emit(req.content, self.url)


class UpdateChecker(core.Object):
    """Check for a new prettyqt version."""

    version_checked = QtCore.Signal(str)  # newest available version
    update_button_clicked = QtCore.Signal(str)  # url to new version
    download_finished = core.Signal(bytes, str)  # response, url
    download_failed = core.Signal(str, str)  # m

    def __init__(
        self,
        parent: QtCore.QObject,
        app_name: str | None = None,
        app_version: str | None = None,
        releases_url: str | None = None,
        pypi_url: str | None = None,
        changelog_url: str | None = None,
        website_url: str | None = None,
        packaged: bool = False,
    ) -> None:
        super().__init__(parent)
        self.packaged = packaged
        self.releases_url = releases_url
        self.pypi_url = pypi_url
        self.changelog_url = changelog_url
        self.website_url = website_url
        self.current_v = app_version or widgets.app().applicationVersion()
        self.app_name = app_name or widgets.app().applicationName()
        self.threadpool = core.ThreadPool()
        self.download_finished.connect(self._on_download_finished)
        self.message_box = widgets.MessageBox()
        self.message_box.set_icon("mdi.download")
        self.message_box.set_standard_buttons(["ok", "cancel"])

        self.message_box.set_default_button("ok")
        if self.changelog_url:
            self.message_box.add_button(
                "Show changelog",
                "accept",
                callback=lambda: webbrowser.open(self.changelog_url),
            )

    def get(self, url: str, timeout: int = 30) -> None:
        logger.debug("Downloading %s...", url)
        worker = Worker(url=url, timeout=timeout)
        worker.signals.download_finished.connect(self.download_finished)
        worker.signals.download_failed.connect(self.download_failed)
        self.threadpool.start(worker)

    @QtCore.Slot(bytes, str)
    def _on_download_finished(self, data: bytes, url: str) -> None:
        """Parse the tag version from the response and emit version retrieved signal."""
        newest_v = None
        try:
            text = data.decode(errors="ignore")
            if self.packaged:
                regex = r"/releases/tag/v(\d+\.\d+\.\d+)\""  # atom
            else:
                regex = r"\"version\":\s*\"(\d+\.\d+\.\d+)\""  # json

            match = re.search(regex, text)
            if match and match[1]:
                newest_v = match[1]
        except Exception as e:
            logger.exception("Parsing response of update check failed: %s", e)

        if not newest_v:
            logger.error("Could not detect remote version. Update check won't work!")
            return
        logger.debug("Newest version: %s (installed: %s)", newest_v, self.current_v)
        self.version_checked.emit(newest_v)
        if core.VersionNumber(newest_v) > core.VersionNumber(self.current_v):
            self._show_update_dialog(new_version=newest_v)

    def _show_update_dialog(self, new_version: str) -> None:
        """Show dialog informing about available update."""
        text = (
            f"<b>{self.app_name} {new_version} is available.</b> "
            f"(Current version: {self.current_v})"
        )
        self.message_box.setText(text)

        info_text = GITHUB_MESSAGE if self.packaged else PYPI_MESSAGE
        self.message_box.setInformativeText(info_text)
        self.message_box.set_cursor("arrow")

        if self.message_box.show_blocking() == "ok":
            update_url = self.releases_url if self.packaged else self.changelog_url
            self.update_button_clicked.emit(update_url)

    def check_for_update(self) -> None:
        """Start the update check."""
        url = f"{self.releases_url}.atom" if self.packaged else f"{self.pypi_url}/json"
        logger.debug("Search for new version on %s", url)
        self.get(url, timeout=10)


if __name__ == "__main__":
    app = widgets.app()
    checker = UpdateChecker(
        app,
        app_version="1.0.0",
        releases_url="https://github.com/phil65/prettyqt/releases",
        changelog_url="https://github.com/phil65/prettyqt/blob/main/CHANGELOG",
        pypi_url="https://pypi.org/pypi/prettyqt",
        website_url="https://github.com/phil65/prettyqt",
    )
    checker.check_for_update()
    app.main_loop()
