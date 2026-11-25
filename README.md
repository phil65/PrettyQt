# PrettyQt: Pythonic layer on top of PyQt6 / PySide6

[![PyPI Latest Release](https://img.shields.io/pypi/v/prettyqt.svg)](https://pypi.org/project/prettyqt/)
[![Package Status](https://img.shields.io/pypi/status/prettyqt.svg)](https://pypi.org/project/prettyqt/)
[![License](https://img.shields.io/pypi/l/prettyqt.svg)](https://github.com/phil65/PrettyQt/blob/main/LICENSE)
[![CodeCov](https://codecov.io/gh/phil65/PrettyQt/branch/main/graph/badge.svg)](https://codecov.io/gh/phil65/PrettyQt)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

**PrettyQt** wraps the complete Qt 6 API (on top of either PyQt6 or PySide6) and makes it
feel like a native Python library: snake_case helpers, strings instead of enums, sensible
type conversions, `__dunder__` methods and many ready-made widgets and models. The
original Qt API keeps working, so you can adopt it incrementally.

**Documentation:** https://phil65.github.io/PrettyQt/

## Installation

PrettyQt needs a Qt binding; pick one via extras:

```sh
pip install "prettyqt[pyside6]"   # or: pip install "prettyqt[pyqt6]"
pip install "prettyqt[pyside6,addons]"   # optional extras (fsspec, pillow, numpy, qtconsole, ...)
```

If both bindings are installed, set `QT_API=pyside6` or `QT_API=pyqt6` to choose.

## Quickstart

```py
from prettyqt import core, custom_widgets, widgets

app = widgets.app()

window = widgets.Widget(window_title="PrettyQt demo")
layout = window.set_layout("vertical", margin=10)

checkbox = widgets.CheckBox("Enable feature")
checkbox.set_checkstate("partial")  # strings instead of enums
assert checkbox.get_checkstate() == "partial"
assert checkbox.checkState() == core.Qt.CheckState.PartiallyChecked  # Qt API still works

button = widgets.PushButton("Click me", icon="mdi.thumb-up")  # icon by name
button.clicked.connect(lambda: print("clicked!"))

layout.add(checkbox)
layout.add(button)
layout.add(custom_widgets.ColorComboBox())

window.show()
app.exec()
```

Every Qt module has a lowercase counterpart without the `Qt` prefix (`QtCore` → `prettyqt.core`,
`QtWidgets` → `prettyqt.widgets`, ...), and every class one without the `Q` prefix
(`QWidget` → `widgets.Widget`). The original Qt classes stay available in the same module
(`widgets.QWidget`).

## Main features

- Subclasses for almost all Qt classes, enriched with helper and `__dunder__` methods.
- Setters/getters accepting strings for enums (`set_checkstate("checked")`), typed with `Literal`s.
- Constructor kwargs in snake_case, with string-to-enum mapping (`widgets.Widget(window_modality="window")`).
- About 80 additional widgets and layouts (`prettyqt.custom_widgets`).
- More than 30 item models and 25 proxy models (`prettyqt.itemmodels`).
- Item delegates, validators, event filters, animations and syntax highlighters.
- Icon fonts (Material Design Icons, FontAwesome, ...) via `prettyqt.iconprovider`.
- Works with PyQt6 and PySide6 through a single, QtPy-like binding layer.

## License

MIT
