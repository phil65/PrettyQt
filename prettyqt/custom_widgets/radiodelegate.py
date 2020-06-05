# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

# based on https://stackoverflow.com/questions/58891116/delegate-with-radio-buttons
# credits to musicamante


from qtpy import QtCore, QtWidgets

from prettyqt import core, gui, widgets


class RadioDelegate(widgets.StyledItemDelegate):
    def __init__(self, owner, chs):
        super().__init__(owner)
        self.items = chs

    def createEditor(self, parent, option, index):
        editor = widgets.Widget(parent)
        editor.setContentsMargins(0, 0, 0, 0)
        editor.setAutoFillBackground(True)
        # create a button group to keep track of the checked radio
        editor.buttonGroup = widgets.ButtonGroup()
        # adding the widget as an argument to the layout constructor automatically
        # applies it to the widget
        layout = widgets.BoxLayout("horizontal", parent=editor)
        layout.setContentsMargins(0, 0, 0, 0)
        for i, k in enumerate(self.items):
            rb = widgets.RadioButton(k)
            layout.addWidget(rb)
            # prevent the radio to get focus from keyboard or mouse
            rb.setFocusPolicy(QtCore.Qt.NoFocus)
            rb.installEventFilter(self)
            editor.buttonGroup.addButton(rb, i)
        # add a stretch to always align contents to the left
        layout.addStretch(1)

        # set a property that will be used for the mask
        editor.setProperty('offMask', gui.Region(editor.rect()))
        editor.installEventFilter(self)
        return editor

    def eventFilter(self, source, event):
        if event.type() == core.Event.MouseButtonPress:
            if isinstance(source, QtWidgets.QRadioButton):
                if not source.parent().hasFocus():
                    # the parent has no focus, set it and ignore the click
                    source.parent().setFocus()
                    return True
            elif not source.hasFocus():
                # the container has been clicked, check
                source.setFocus()
        elif event.type() == core.Event.FocusIn:
            # event received as a consequence of setFocus
            # clear the mask to show it completely
            source.clearMask()
        elif event.type() == core.Event.FocusOut:
            # another widget has requested focus, set the mask
            source.setMask(source.property('offMask'))
            # update the table viewport to get rid of possible
            # grid lines left after masking
            source.parent().update()
        return super().eventFilter(source, event)

    def updateEditorGeometry(self, editor, option, index):
        rect = core.Rect(option.rect)
        minWidth = editor.minimumSizeHint().width()
        if rect.width() < minWidth:
            rect.setWidth(minWidth)
        editor.setGeometry(rect)
        # create a new mask based on the option rectangle, then apply it
        mask = gui.Region(0, 0, option.rect.width(), option.rect.height())
        editor.setProperty('offMask', mask)
        editor.setMask(mask)

    def setEditorData(self, editor, index):
        value = index.data(QtCore.Qt.DisplayRole)
        if value in self.items:
            editor.buttonGroup.button(self.items.index(value)).setChecked(True)

    def setModelData(self, editor, model, index):
        button = editor.buttonGroup.checkedId()
        if button >= 0:
            model.setData(index, self.items[button], QtCore.Qt.DisplayRole)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    widget = widgets.TableWidget()
    widget.setColumnCount(3)
    widget.insertRow(0)
    widget.setHorizontalHeaderLabels(['LIB', 'CELL', 'area'])
    item = widgets.TableWidgetItem("test")
    widget.setItem(0, 0, item)
    widget.setItem(1, 1, widgets.TableWidgetItem("test"))
    delegate = RadioDelegate(widget, ["a", "b"])
    widget.setItemDelegateForColumn(0, delegate)
    widget.openPersistentEditor(item)
    widget.show()
    app.exec_()
