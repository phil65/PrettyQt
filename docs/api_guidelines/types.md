PrettyQt loosens type restrictions for the Qt API calls. Here is a short list how support for types is extended:


**QtGui.QColor**

* `Sequence[int, int, int]`
* `Sequence[int, int, int, int]`
* `str` (Color name or #color hex value)
* `str` (Color role from palette. Example* "window_role", "highlight_role")

Example:
```py
effect = widgets.GraphicsColorizeEffect()
effect.set_color("window_role")
effect.set_color((30, 30, 50))
effect.set_color("green")
```

**QtGui.QIcon**

* `pathlib.Path` (path to an icon)
* `str` (icon name, like "mdi.information")

Example:
```py
button = widgets.PushButton()
button.set_icon("mdi.information")
button.set_icon(pathlib.Path("path/to/icon.png"))
```

**QtCore.QTime**

* `datetime.time` (https://docs.python.org/3/library/datetime.html#datetime.time)
* `str` (which can be parsed from dat)

Example:
```py
widget = widgets.TimeEdit()
widget.set_time("02:04:00")
```

**QtCore.QRegularExpression**

* `str` (containing the regex pattern)
* `re.Pattern`

Example:
```py
proxy = core.SortFilterProxyModel()
pattern = re.complile("[a-z]")
proxy.set_filter_regular_expression(pattern)
```

**QtCore.QUrl**

* `str`
* `os.PathLike` (when appropriate)
* `urllib.parse.ParseResult`

Example:
```py
page = webenginecore.WebEnginePage()
page.set_url("http://www.github.com/phil65/prettyqt")
```

**QtCore.QByteArray**

* `str`
* `bytes`

Example:
```py
animation = core.PropertyAnimation()
animation.set_property_animation("pos")
```

**QtCore.QMargins**

* `tuple[int, int, int, int]` (left, top, right, bottom)
* `tuple[int, int]` (left/right, top/bottom)
* `int`
* `None` (same as 0)
* `QtCore.QMarginsF`

Example:
```py
chart = charts.Chart()
chart.set_margins((4, 2, 0, 0))
chart.set_margins((1, 2))
chart.set_margins(5)
chart.set_margins(None)
```

**QtCore.QPoint**

* `tuple[int, int]`
* `QtCore.QPointF`

Example:
```py
point = core.Line()
point.set_p1((4, 2))
```

**QtCore.QPointF**

* `tuple[float, float]`
* `tuple[int, int]`
* `QtCore.QPoint`

**QtCore.QSize**

* `tuple[int, int]`
* `QtCore.QSizeF`

**QtCore.QSizeF**

* `tuple[float, float]`
* `QtCore.QSize`

