# -*- coding: utf-8 -*-
"""
"""

import logging

from prettyqt import core, widgets


logger = logging.getLogger(__name__)


class CheckBoxDelegate(widgets.ItemDelegate):
    """
    A delegate that places a fully functioning CheckBox in every
    cell of the column to which it's applied
    """

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.selected = []

    def createEditor(self, parent, option, index):
        """
        override
        instanciate the editor widget and initialize it
        also connect currentIndexChanged signal
        """
        cb = widgets.CheckBox(parent)
        cb.currentIndexChanged.connect(self.currentIndexChanged)
        return cb

    def setEditorData(self, cb, index):
        """
        override
        set correct initial value for editor widget
        """
        current_selection = index.data()
        with cb.block_signals():
            cb.setCurrentText(current_selection)

    def setModelData(self, combo, model, index):
        """
        override, gets called on self.commitData (?)
        apply the newly selected dtype to the column if possible
        """
        dtype = self.dtypes[combo.currentText()]
        # s = model.data(index, model.DATA_ROLE)
        try:
            model.setData(index, dtype, model.DTYPE_ROLE)
        except ValueError as e:
            logger.error(e)

    @core.Slot()
    def currentIndexChanged(self):
        self.commitData.emit(self.sender())
