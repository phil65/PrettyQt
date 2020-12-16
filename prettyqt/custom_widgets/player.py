import sys
from typing import Optional

from qtpy import QtWidgets

from prettyqt import constants, core, gui, multimedia, multimediawidgets, widgets


class Player(widgets.MainWindow):
    def __init__(self, parent: Optional[QtWidgets.QWidget] = None):
        super().__init__(parent)
        self.playback_rate = 1.0
        self.playlist = multimedia.MediaPlaylist(self)
        self.player = multimedia.MediaPlayer(self)

        toolbar = widgets.ToolBar()
        self.addToolBar(toolbar)

        file_menu = self.menuBar().add_menu("&File")
        open_action = widgets.Action(
            icon=gui.Icon.fromTheme("document-open"),
            text="&Open...",
            parent=self,
            shortcut=gui.KeySequence.Open,
            callback=self.open,
        )
        exit_action = widgets.Action(
            icon=gui.Icon.fromTheme("application-exit"),
            text="E&xit",
            parent=self,
            shortcut="Ctrl+Q",
            callback=self.close,
        )

        play_menu = self.menuBar().add_menu("&Play")
        self.play_action = toolbar.add_action(
            icon=widgets.Application.get_style_icon("media_play"),
            label="Play",
            callback=self.player.play,
        )
        self.previous_action = toolbar.add_action(
            icon=widgets.Application.get_style_icon("media_skip_backward"),
            label="Previous",
            callback=self.previous_clicked,
        )
        self.pause_action = toolbar.add_action(
            icon=widgets.Application.get_style_icon("media_pause"),
            label="Pause",
            callback=self.player.pause,
        )
        self.next_action = toolbar.add_action(
            icon=widgets.Application.get_style_icon("media_skip_backward"),
            label="Next",
            callback=self.playlist.next,
        )

        self.stop_action = toolbar.add_action(
            icon=widgets.Application.get_style_icon("media_stop"),
            label="Stop",
            callback=self.player.stop,
        )
        file_menu.add(open_action)
        file_menu.add(exit_action)

        play_menu.add(self.play_action)
        play_menu.add(self.previous_action)
        play_menu.add(self.pause_action)
        play_menu.add(self.next_action)
        play_menu.add(self.stop_action)

        self.clock = widgets.Label(self)
        self.clock.setText("00:00/00:00")
        # self.clock.setGeometry(550, 660, 80, 30)

        self.vol_slider = widgets.Slider()
        self.vol_slider.set_orientation("horizontal")
        self.vol_slider.set_range(0, 100)
        self.vol_slider.setFixedWidth(120)
        self.vol_slider.set_value(self.player.volume())
        self.vol_slider.setTickInterval(10)
        self.vol_slider.set_tick_position("below")
        self.vol_slider.setToolTip("Volume")
        self.vol_slider.value_changed.connect(self.player.setVolume)

        self.slider = widgets.Slider(constants.HORIZONTAL, self)
        # self.slider.setGeometry(10, 640, 800 - 20, 20)
        self.slider.setRange(0, 100)
        self.slider.value_changed.connect(self.on_slider_change)

        toolbar.add_separator()
        toolbar.addWidget(self.vol_slider)
        toolbar.add_separator()
        toolbar.addWidget(self.clock)
        toolbar.add_separator()
        toolbar.addWidget(self.slider)

        self.video_widget = multimediawidgets.VideoWidget()
        self.setCentralWidget(self.video_widget)
        self.player.setPlaylist(self.playlist)
        self.player.stateChanged.connect(self._update_buttons)
        self.player.setVideoOutput(self.video_widget)
        self.player.positionChanged.connect(self.on_player_change)
        self.player.durationChanged.connect(self.set_media_time)

        self._update_buttons(self.player.state())

    def handle_backward(self):
        if self.playback_rate > 0.5:
            self.playback_rate = self.playback_rate - 0.5
            self.player.setPlaybackRate(self.playback_rate)

    def handle_forward(self):
        if self.playback_rate < 1.5:
            self.playback_rate = self.playback_rate + 0.5
            self.player.setPlaybackRate(self.playback_rate)

    def set_media_time(self, time):
        self.slider.set_value(0)
        self.time = self.player.duration() / 1000
        self.slider.setRange(0, int(self.time))

    def on_player_change(self, val: int):
        with self.slider.block_signals():
            self.slider.set_value(int(val / 1000))
        tmp = self.player.position()
        duration = self.player.duration() / 1000
        # print(tmp, val)
        secs = tmp / 1000
        self.clock.setText(
            "%02d:%02d / %02d:%02d" % (secs / 60, secs % 60, duration / 60, duration % 60)
        )

    def on_slider_change(self, val):
        self.player.setPosition(self.slider.get_value() * 1000)

    def open(self):
        file_dialog = widgets.FileDialog(parent=self)
        # supportedMimeTypes = ["video/mp4", "*.*"]
        # file_dialog.setMimeTypeFilters(supportedMimeTypes)
        movies_location = core.StandardPaths.get_writable_location("movies")
        file_dialog.set_directory(movies_location)
        if file_dialog.exec_() == widgets.Dialog.Accepted:
            self.playlist.add_media(file_dialog.selectedFiles()[0])
            self.player.play()

    def previous_clicked(self):
        # Go to previous track if we are within the first 5 seconds of playback
        # Otherwise, seek to the beginning.
        if self.player.position() <= 5000:
            self.playlist.previous()
        else:
            self.player.setPosition(0)

    def _update_buttons(self, state):
        media_count = len(self.playlist)
        self.play_action.setEnabled(
            media_count > 0 and state != multimedia.MediaPlayer.PlayingState
        )
        self.pause_action.setEnabled(state == multimedia.MediaPlayer.PlayingState)
        self.stop_action.setEnabled(state != multimedia.MediaPlayer.StoppedState)
        self.previous_action.setEnabled(self.player.position() > 0)
        self.next_action.setEnabled(media_count > 1)


if __name__ == "__main__":
    app = widgets.app()
    mainWin = Player()
    mainWin.resize(800, 600)
    mainWin.show()
    sys.exit(app.main_loop())
