from qtpy import QtWidgets

from prettyqt import widgets


QtWidgets.QScrollArea.__bases__ = (widgets.AbstractScrollArea,)


class ScrollArea(QtWidgets.QScrollArea):
    def serialize_fields(self):
        return dict(widget=self.widget(), resizable=self.widgetResizable())

    def __setstate__(self, state):
        self.set_widget(state["widget"])
        self.setWidgetResizable(state["resizable"])

    def __reduce__(self):
        return type(self), (), self.__getstate__()

    def set_widget(self, widget):
        self.setWidget(widget)
