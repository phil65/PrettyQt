Animating
======

PrettyQt makes it easy to animate your widgets.
All animation-related methods are available via the Widget.fx attribute.

## some Examples:

    widget = widgets.Widget()
    # start a fade-in animation
    widget.fx["windowOpacity"].animate(start=0, end=1, duration=1000)
    # fade-in when widget gets clicked
    widget.fx["windowOpacity"].animate_on_event("mouse_button_press", start=0, end=1)

    # convenience method for mentioned fad-in
    widget.fx.fade_in(start=0, end=1, start=500)

    # start a zoom animation
    widget.fx.zoom(start=1, end=1.5, duration=400)

    # start a slide animation 100px to the right
    widget.fx.slide(start=(0, 0), end=(100, 0), duration=400)
