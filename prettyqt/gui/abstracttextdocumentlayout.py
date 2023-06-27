from __future__ import annotations

from prettyqt import constants, core
from prettyqt.qt import QtGui
from prettyqt.utils import datatypes, get_repr


class AbstractTextDocumentLayoutMixin(core.ObjectMixin):
    def __repr__(self):
        return get_repr(self)

    def __len__(self):
        return self.pageCount()

    def get_block_bounding_rect(self, block: QtGui.QTextBlock) -> core.RectF:
        return core.RectF(self.blockBoundingRect(block))

    def get_frame_bounding_rect(self, frame: QtGui.QTextBlock) -> core.RectF:
        return core.RectF(self.frameBoundingRect(frame))

    def hit_test(self, point: datatypes.PointFType, fuzzy: bool = False) -> int | None:
        accuracy = (
            constants.HitTestAccuracy.FuzzyHit
            if fuzzy
            else constants.HitTestAccuracy.ExactHit
        )
        result = self.hitTest(datatypes.to_pointf(point), accuracy)
        return None if result == -1 else result


class AbstractTextDocumentLayout(
    AbstractTextDocumentLayoutMixin, QtGui.QAbstractTextDocumentLayout
):
    pass


if __name__ == "__main__":
    from prettyqt import gui

    doc = gui.TextDocument()
    layout = AbstractTextDocumentLayout(doc)
