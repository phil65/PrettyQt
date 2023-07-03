The proxifier object offers a more declarative way to set up proxy models.

``` py
model = MyTableModel()
table = widgets.TableView()
table.set_model(model)

# lets change the appearance a bit.
# Set the font color of column 2 and 3 to red and font to Courier.

table.proxifier[:, 2:4].style(foreground="red", font="Courier")

# Cut off last column and only show last 50 lines.
table.proxifier[:50, :-1].filter()

# Set first 20 lines of these 50 lines to read_only
table.proxifier[:20, :].change_flags(editable=False)

# Make first column checkable and trigger callback on checkstate change.
table.proxifier[0].make_checkable(callback=my_callback)
```

::: prettyqt.utils.proxifier.Proxifier
