"""Tests for `datacook` package."""

# import pytest

import pytest

from prettyqt import widgets


@pytest.fixture
def tablewidget():
    widget = widgets.TableWidget()
    widget.setColumnCount(3)
    widget.insertRow(0)
    widget.setHorizontalHeaderLabels(["LIB", "CELL", "area"])
    item = widgets.TableWidgetItem("test")
    widget.setItem(0, 0, item)
    widget.setItem(1, 1, widgets.TableWidgetItem("test"))
    return widget
