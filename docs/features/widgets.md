Since this library is huge, I will try to give an overview about some modules and mention some of the included "highlights".


- All setters and getters for Enum properties have an equivalent method taking a string:

```py
widget = QtWidgets.QWidget()
widget.setSizeAdjustPolicy(widget.SizeAdjustPolicy.AdjustToContents)
```
becomes:

```py
widgets = widgets.Widget()
widget.set_size_adjust_policy("adjust_to_contents")
```

Everything is fully typed with Literals, so you should get a very nice IDE experience.

The same also applies to getters, with the rule that everything is prefixed with "get_" in order to avoid name collisions.

```py
assert widget.sizeAdjustPolicy() == widget.SizeAdjustPolicy.AdjustToContents
```
becomes
```py
assert widget.get_size_adjust_policy() == "adjust_to_contents"
```

Note that these new setters and getters are "optional" to use. The "old" methods are still fully accessible. As a general rule, the library tries to be 100% "backwards-compatible".




Slicing:

A lot of QObjects fully support slicing via __getitem__.
To allow easy batch manipulation, the returned list can delegate method calls to all of its members.

## Some Examples:
```py
model = AVeryNiceTableModel()

# get indexes of first row:
indexes = model[:, 0]

# get indexes of very second column
indexes = model[:, ::2]

# batch operations:
# return list containing data from UserRole for given slice.
data = model[2:5, 1:10:2].data(constants.USER_ROLE)

# now we check out the same for widgets.
# lets say we have a HBoxLayout containing many items.

layout = widgets.HBoxLayout()
... # populate it with many widgets.

# Only show first 5 widgets.
layout[5:].set_visible(False)

# get a list containing the width of every 2nd widget in the layout.
widths = layout[::2].width()

# trigger a fade-in animation for first 3 widgets
layout[:3].fx.fade_in(duration=1000)
```

Validators:

PrettyQt ships a large number of predefined validators.


    # Validators can also be combined. The resulting CompositeValidator checks if all containing validators accept the input.

    # set_validator also gained a non-strict mode.
    # That way the "lowest" result of the validator becomes "Intermediate", since the Qt behaviour of ignoring keypresses when state goes to invalid might not be wanted.




