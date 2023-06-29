Animating
======

PrettyQt makes it easy to animate your widgets.
All animation-related methods are available via the Widget.fx attribute.
Easy one-liners to bring

## some Examples:
```py
# a lot of animations depend on current geometry.
# It´s advisable to show widget first so that it gets layouted.
widget = widget.Label("I will get animated.")
widget.show()

# start a general fade animation with fixed start/end
widget.fx["windowOpacity"].animate(start=0, end=1, duration=1000)

# Transition widget size from current value to (500, 500)
widget.fx["size"].transition_to((500, 500), duration=1000)

# Transition widget size from current value to (500, 500)
widget.fx["pos"].transition_from((0, -100), duration=1000)

# fade-in when widget gets clicked
widget.fx["windowOpacity"].animate_on_event("mouse_button_press", start=0, end=1)

# convenience method for mentioned fade-in
widget.fx.fade_in(start=0, end=1, start=500)

# start a zoom animation
widget.fx.zoom(start=1, end=1.5, duration=400)

# start a slide animation 100px to the right
widget.fx.slide(start=(0, 0), end=(100, 0), duration=400)
```

Animating stylesheet values is also possible easily:

TODO.







