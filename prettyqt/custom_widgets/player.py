import sys
from prettyqt import gui, core, multimedia, widgets, multimediawidgets


class Player(widgets.MainWindow):
    def __init__(self):
        super().__init__()

        self.playlist = multimedia.MediaPlaylist()
        self.player = multimedia.MediaPlayer()

        toolbar = widgets.ToolBar()
        self.addToolBar(toolbar)

        file_menu = self.menuBar().addMenu("&File")
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

        play_menu = self.menuBar().addMenu("&Play")
        self.play_action = toolbar.add_action(
            icon=widgets.Application.get_icon("media_play"),
            label="Play",
            callback=self.player.play,
        )
        self.previous_action = toolbar.add_action(
            icon=widgets.Application.get_icon("media_skip_backward"),
            label="Previous",
            callback=self.previous_clicked,
        )
        self.pause_action = toolbar.add_action(
            icon=widgets.Application.get_icon("media_pause"),
            label="Pause",
            callback=self.player.pause,
        )
        self.next_action = toolbar.add_action(
            icon=widgets.Application.get_icon("media_skip_backward"),
            label="Next",
            callback=self.playlist.next,
        )

        self.stop_action = toolbar.add_action(
            icon=widgets.Application.get_icon("media_stop"),
            label="Stop",
            callback=self.player.stop,
        )
        file_menu.addAction(open_action)
        file_menu.addAction(exit_action)

        play_menu.addAction(self.play_action)
        play_menu.addAction(self.previous_action)
        play_menu.addAction(self.pause_action)
        play_menu.addAction(self.next_action)
        play_menu.addAction(self.stop_action)

        self.vol_slider = widgets.Slider()
        self.vol_slider.set_orientation("horizontal")
        self.vol_slider.setMinimum(0)
        self.vol_slider.setMaximum(100)
        self.vol_slider.setFixedWidth(120)
        self.vol_slider.setValue(self.player.volume())
        self.vol_slider.setTickInterval(10)
        self.vol_slider.set_tick_position("below")
        self.vol_slider.setToolTip("Volume")
        self.vol_slider.valueChanged.connect(self.player.setVolume)
        toolbar.addWidget(self.vol_slider)

        self.video_widget = multimediawidgets.VideoWidget()
        self.setCentralWidget(self.video_widget)
        self.player.setPlaylist(self.playlist)
        self.player.stateChanged.connect(self._update_buttons)
        self.player.setVideoOutput(self.video_widget)

        self._update_buttons(self.player.state())

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
    sys.exit(app.exec_())
