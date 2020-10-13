from qtpy import QtMultimedia

from prettyqt import constants, core


class PlaylistModel(core.AbstractItemModel):

    HEADER = ["Name"]

    def __init__(self, parent=None):
        super().__init__(parent)
        self._playlist = None

    def rowCount(self, parent=core.ModelIndex()):
        return (
            self._playlist.mediaCount()
            if self._playlist is not None and not parent.isValid()
            else 0
        )

    def columnCount(self, parent=core.ModelIndex()):
        return len(self.HEADER) if not parent.isValid() else 0

    def index(self, row, column, parent=core.ModelIndex()):
        return (
            self.createIndex(row, column)
            if self._playlist is not None
            and not parent.isValid()
            and 0 <= row < self._playlist.mediaCount()
            and 0 <= column < len(self.HEADER)
            else core.ModelIndex()
        )

    def parent(self, child):
        return core.ModelIndex()

    def data(self, index, role=constants.DISPLAY_ROLE):
        if index.isValid() and role == constants.DISPLAY_ROLE:
            if index.column() == 0:
                location = self._playlist.media(index.row()).canonicalUrl()
                return core.FileInfo(location.path()).fileName()

            return self.m_data[index]

        return None

    def playlist(self) -> QtMultimedia.QMediaPlaylist:
        return self._playlist

    def set_playlist(self, playlist: QtMultimedia.QMediaPlaylist):
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
