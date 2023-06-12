Layouts
======



## Models for Python types

### Context manager to build layouts


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


### Setting a layout

Layouts can be set by an identifier:

    layout = widget.set_layout("horizontal")

Available layouts:
- "horizontal"
- "vertical"
- "grid"
- "horizontal"
- "horizontal"
- "horizontal"
- "horizontal"
- "horizontal"
- "horizontal"

