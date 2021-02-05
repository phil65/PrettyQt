from __future__ import annotations

from prettyqt import core
from prettyqt.qt import QtCore, QtGui


QtGui.QAbstractTextDocumentLayout.__bases__ = (core.Object,)


class AbstractTextDocumentLayout(QtGui.QAbstractTextDocumentLayout):
    def __repr__(self):
        return f"{type(self).__name__}()"

    def __len__(self):
        return self.pageCount()

    def get_block_bounding_rect(self, block: QtGui.QTextBlock) -> core.RectF:
        return core.RectF(self.blockBoundingRect(block))

    def get_frame_bounding_rect(self, frame: QtGui.QTextBlock) -> core.RectF:
        return core.RectF(self.frameBoundingRect(frame))

    def hit_test(
        self, point: core.PointF | tuple[float, float], fuzzy: bool = False
    ) -> int | None:
        if isinstance(point, tuple):
            point = core.PointF(*point)
        accuracy = QtCore.Qt.FuzzyHit if fuzzy else QtCore.Qt.ExactHit
        result = self.hitTest(point, accuracy)
        if result == -1:
            return None
        return result


if __name__ == "__main__":
    from prettyqt import gui

    doc = gui.TextDocument()
    layout = AbstractTextDocumentLayout(doc)
