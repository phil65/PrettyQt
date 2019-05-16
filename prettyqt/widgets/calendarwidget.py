# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from bidict import bidict
from qtpy import QtWidgets

from prettyqt import widgets

SELECTION_MODES = bidict(dict(none=QtWidgets.QCalendarWidget.NoSelection,
                              single=QtWidgets.QCalendarWidget.SingleSelection))

HEADER_FORMATS = bidict(dict(none=QtWidgets.QCalendarWidget.NoVerticalHeader,
                             week_numbers=QtWidgets.QCalendarWidget.ISOWeekNumbers))


class CalendarWidget(QtWidgets.QCalendarWidget):

    def __getstate__(self):
        return dict(date=self.selectedDate())

    def __setstate__(self, state):
        self.__init__()
        self.setSelectedDate(state["date"])

    def get_value(self):
        return self.selectedDate()

    def set_value(self, value):
        self.setSelectedDate(value)


CalendarWidget.__bases__[0].__bases__ = (widgets.Widget,)


if __name__ == "__main__":
    app = widgets.app()
    w = CalendarWidget()
    w.show()
    app.exec_()
