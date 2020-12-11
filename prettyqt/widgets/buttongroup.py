from qtpy import QtWidgets


class ButtonGroup(QtWidgets.QButtonGroup):
    def __getitem__(self, index: int) -> QtWidgets.QAbstractButton:
        return self.button(index)
