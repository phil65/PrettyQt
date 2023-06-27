To allow for an easy switch, the API layer provided by PrettyQt should be consistent and predictable. When knowing the following guidelines, it should be easy to guess how PrettyQt can be used:

1. Every Qt namespace has an equivalent module, named lowerase and with the Qt-prefix removed.
Example: QtCore basically equals to prettyqt.core

2. Every Qt class has an equivalent class with the Q-prefix removed, placed in the namespace mentioned above. The "original" Qt classes are still available in the same module.
- Example: widgets.Widget is the QWidget subclass also containing the mixins, widgets.QWidget is the original Qt Class.

3. The Qt-inherited API should still work as-is. If any method is overriden by this framework, it should still be allowed to call it with the original Qt signature.

4. Naming of the equivalent PrettyQt methods should follow a consistent scheme. Setters are lower-cased and snake-cased, getters are lower-cased, snake-cased and have a get_ prepended to avoid name clashes.
If any lower-cased, snake-cased method name is not provided by PrettyQt, it will call the original method via __getattr__. (The last point only applies to classes which inherit from QObject.)



Types

PrettyQt loosens type restrictions for all API calls.

Here is a short list how support for types is extended:

QtGui.QColor:
- Sequence[int, int, int]
- Sequence[int, int, int, int]
- str (Color name or #color hex value)
- str (Color role from palette. Example: "window_role", "highlight_role")

Example:
    effect = widgets.GraphicsColorizeEffect()
    effect.set_color("window_role")
    effect.set_color((30, 30, 50))
    effect.set_color("green")

QtGui.QIcon:
- pathlib.Path (path to an icon)
- str (icon name, like "mdi.information")

Example:
    button = widgets.PushButton()
    button.set_icon("mdi.information")
    button.set_icon(pathlib.Path("path/to/icon.png"))

QtCore.QTime:
- datetime.time (https://docs.python.org/3/library/datetime.html#datetime.time)
- str (which can be parsed from dat)

Example:
    widget = widgets.TimeEdit()
    widget.set_time("02:04:00")

QtCore.QRegularExpression:
- str (containing the regex pattern)
- re.Pattern

Example:
    proxy = core.SortFilterProxyModel()
    pattern = re.complile("[a-z]")
    proxy.set_filter_regular_expression(pattern)

QtCore.QUrl:
- str
- os.PathLike (when appropriate)
- urllib.parse.ParseResult

Example:
    page = webenginecore.WebEnginePage()
    page.set_url("http://www.github.com/phil65/prettyqt")

QtCore.QByteArray
- str
- bytes

QtCore.QMargins
- tuple[int, int, int, int] (left, top, right, bottom)
- tuple[int, int] (left/right, top/bottom)
- int
- None (same as 0)
- QtCore.QMarginsF

QtCore.QPoint:
- tuple[int, int]
- QtCore.QPointF

QtCore.QPointF:
- tuple[float, float]
- tuple[int, int]
- QtCore.QPoint

QtCore.QSize:
- tuple[int, int]
- QtCore.QSizeF

QtCore.QSizeF:
- tuple[float, float]
- QtCore.QSize

