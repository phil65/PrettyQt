from __future__ import annotations

import logging

import requests

from prettyqt import core


logger = logging.getLogger(__name__)


class WorkerSignals(core.Object):
    """TrayMenus' communication bus."""

    download_finished = core.Signal(bytes, str)  # response, url
    download_failed = core.Signal(str, str)  # msg, url


class DownloadWorker(core.QRunnable):
    def __init__(self, url: str, timeout: int = 30) -> None:
        super().__init__()
        self.url = url
        self.timeout = timeout
        self.signals = WorkerSignals()

    @core.Slot()
    def run(self) -> None:
        try:
            req = requests.get(self.url, verify=True, timeout=self.timeout)
        except Exception as e:
            msg = f"Exception '{e}' during download of '{self.url}'"
            logger.exception(msg)
            self.signals.download_failed.emit(msg, self.url)
        else:
            self.signals.download_finished.emit(req.content, self.url)


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    pool = core.ThreadPool()
    worker = DownloadWorker("https://api.thecatapi.com/v1/images/search")
    worker.signals.download_finished.connect(print)
    worker.signals.download_finished.connect(app.quit)
    pool.start(worker)
    app.exec()
