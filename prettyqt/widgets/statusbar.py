from __future__ import annotations

from prettyqt import core, widgets
from prettyqt.qt import QtGui


class StatusBar(widgets.WidgetMixin, widgets.QStatusBar):
    """Horizontal bar suitable for presenting status information."""

    def __add__(self, other: QtGui.QAction | widgets.QWidget) -> StatusBar:
        match other:
            case QtGui.QAction():
                self.addAction(other)
                return self
            case widgets.QWidget():
                self.addWidget(other)
                return self
            case _:
                raise TypeError(other)

    def add_threadpool_info(self, threadpool: core.ThreadPool):
        class ThreadPoolLabel(widgets.Label):
            def update_job_count(self, num_jobs: int):
                text = f"Running jobs: {num_jobs}" if num_jobs > 0 else "No running jobs"
                self.set_text(text)

        status_label = ThreadPoolLabel(self)
        threadpool.job_num_updated.connect(status_label.update_job_count)
        status_label.update_job_count(threadpool.activeThreadCount())
        progress_bar = widgets.ProgressBar(self, text_visible=False)
        progress_bar.hide()
        progress_bar.setRange(0, 0)
        progress_bar.setFixedSize(200, 20)
        threadpool.busy_state_changed.connect(progress_bar.setVisible)
        self.addPermanentWidget(status_label)
        self.addPermanentWidget(progress_bar)

    def add_widget(self, widget: widgets.QWidget, permanent: bool = False) -> None:
        if permanent:
            self.addPermanentWidget(widget)
        else:
            self.addWidget(widget)

    def show_message(self, message: str, timeout: int = 0) -> None:
        self.showMessage(message, timeout)


if __name__ == "__main__":
    app = widgets.app()
    dlg = widgets.MainWindow()
    status_bar = StatusBar()
    status_bar.set_color("black")
    label = widgets.Label("test")
    status_bar.addWidget(label)
    dlg.setStatusBar(status_bar)
    dlg.show()
    app.exec()
