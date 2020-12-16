from typing import Optional

from qtpy import QtCore, QtMultimedia

from prettyqt import constants, core


class PlaylistModel(core.AbstractTableModel):

    HEADER = ["Name"]

    def __init__(self, parent: Optional[QtCore.QObject] = None):
        super().__init__(parent)
        self._playlist = None

    def rowCount(self, parent=None):
        if self._playlist is None:
            return 0
        return len(self._playlist)

    def columnCount(self, parent=None):
        return len(self.HEADER)

    def data(self, index: core.ModelIndex, role=constants.DISPLAY_ROLE):
        if not index.isValid():
            return None
        if self._playlist is None:
            return None
        if role == constants.DISPLAY_ROLE:
            if index.column() == 0:
                location = self._playlist.media(index.row()).canonicalUrl()
                return core.FileInfo(location.path()).fileName()
        return None

    def get_playlist(self) -> Optional[QtMultimedia.QMediaPlaylist]:
        return self._playlist

    def set_playlist(self, playlist: Optional[QtMultimedia.QMediaPlaylist]):
        if self._playlist is not None:
            self._playlist.mediaAboutToBeInserted.disconnect(self.beginInsertItems)
            self._playlist.mediaInserted.disconnect(self.endInsertRows)
            self._playlist.mediaAboutToBeRemoved.disconnect(self.beginRemoveItems)
            self._playlist.mediaRemoved.disconnect(self.endRemoveRows)
            self._playlist.mediaChanged.disconnect(self.change_items)

        with self.reset_model():
            self._playlist = playlist

            if self._playlist is not None:
                self._playlist.mediaAboutToBeInserted.connect(
                    lambda x, y: self.beginInsertRows(core.ModelIndex(), x, y)
                )
                self._playlist.mediaInserted.connect(self.endInsertRows)
                self._playlist.mediaAboutToBeRemoved.connect(
                    lambda x, y: self.beginRemoveRows(core.ModelIndex(), x, y)
                )
                self._playlist.mediaRemoved.connect(self.endRemoveRows)
                self._playlist.mediaChanged.connect(self.change_items)

    def change_items(self, start: int, end: int):
        self.dataChanged.emit(self.index(start, 0), self.index(end, len(self.HEADER)))


if __name__ == "__main__":
    from prettyqt import multimedia, widgets

    URL = (
        "http://commondatastorage.googleapis.com/"
        "gtv-videos-bucket/sample/BigBuckBunny.mp4"
    )

    app = widgets.app()
    tableview = widgets.TableView()
    model = PlaylistModel()
    playlist = multimedia.MediaPlaylist()
    playlist.add_media(URL)
    model.set_playlist(playlist)
    tableview.set_model(model)
    print(model.rowCount(), model.columnCount())
    print(model._playlist)
    tableview.show()
    app.main_loop()
