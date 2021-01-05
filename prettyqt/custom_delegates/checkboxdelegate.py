from __future__ import annotations

import logging

from prettyqt import core, widgets


logger = logging.getLogger(__name__)


class CheckBoxDelegate(widgets.ItemDelegate):
    """Delegate that places a CheckBox in every cell."""

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.selected = []

    def createEditor(self, parent, option, index):
        """Override.

        instanciate the editor widget and initialize it
        also connect currentIndexChanged signal.
        """
        cb = widgets.CheckBox(parent)
        cb.currentIndexChanged.connect(self.currentIndexChanged)
        return cb

    def setEditorData(self, cb, index):
        """Override.

        set correct initial value for editor widget
        """
        current_selection = index.data()
        with cb.block_signals():
            cb.setCurrentText(current_selection)

    @core.Slot()
    def currentIndexChanged(self):
        self.commitData.emit(self.sender())
