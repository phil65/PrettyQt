### Context manager to build layouts

```py
from prettyqt import widgets

widget = widgets.Widget()
layout = widget.set_layout("horizontal")
with layout.get_sub_layout("splitter", orientation="horizontal") as layout:
    with layout.get_sub_layout("flow") as layout:
        layout += widgets.PushButton("Flow 1")
        layout += widgets.RadioButton("Flow 2")
        layout += widgets.PushButton("Flow 3")
        layout += widgets.RadioButton("Flow 4")
    layout += widgets.PlainTextEdit("Splitter middle")
    layout += widgets.PlainTextEdit("Splitter right")
    with layout.get_sub_layout("splitter", orientation="vertical") as layout:
        layout += widgets.PlainTextEdit("Splitter top")
        layout += widgets.PlainTextEdit("Splitter middle")
        with layout.get_sub_layout("scroll", orientation="vertical") as layout:
            layout += widgets.PlainTextEdit("ScrollArea top")
            layout += widgets.PlainTextEdit("ScrollArea middle")
            button = layout.add(widgets.PushButton("ScrollArea Bottom"))
with layout.get_sub_layout("horizontal") as layout:
    layout += widgets.PlainTextEdit("HorizontalLayout left")
    layout += widgets.PlainTextEdit("HorizontalLayout right")
    with layout.get_sub_layout("grid") as layout:
        layout[0, 0] = widgets.PushButton("Grid topleft")
        layout[0, 1] = widgets.RadioButton("Grid topright")
        layout[1, 0:1] = widgets.PushButton("Grid bottom")
        layout += widgets.RadioButton("Flow 4")
```

### Setting a layout

Layouts can be also be set by an identifier:

```py
layout = widget.set_layout("horizontal")
# equals
layout = widgets.HBoxLayout()
widget.set_layout(layout)
```
Available layouts:

- Qt layouts:
    - "horizontal"
    - "vertical"
    - "grid"
    - "form"
    - "stacked"


- custom layouts:
    - "multiline"
    - "border"
    - "flow"

### Accessing widgets inside a layout

All layouts support slicing, including the possibility to apply batch operations:

```py
widgets = layout[:4]  # take the first 4 widgets
widgets = layout[::2] # take every second widget

widgets[2:8:2].set_visible(False)  # hide widgets with index 2, 4, 6, 8
sizes = widgets[5:].size()  # returns a list with the sizes of widget with index 5 and following.
```

As shown, operations on slices are forwarded to each widget which is part of the slice. No need to loop over the whole layout.

The same principles also apply to splitters, toolboxes and TabWidgets.

```py
splitter[2:5].set_font("Consolas")
```

