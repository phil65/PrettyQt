(Example: high numbers red, low numbers green).
: To color cells, this proxy needs a minimum and maximum value. Three modes are available:
: Let the user choose a min max value.
: Use min max value from currently visible table section.
: use min max value from "seen" table content. (meaning that the model adapts min max values based.)

The last two modes have the advantage that nothing needs to be computed in advance, min/max values are calculated on-the fly.

Possible modes are:
- All: Highlight all cells within given slice
- Column: Highlight all cells of same column as current if cell is within given slice.
- Row: Highlight all cells of same row as current if cell is within given slice.

!!! note
    This is a slice proxy and can be selectively applied to a model.

### Example

```py
model = MyModel()
table = widgets.TableView()
table.set_model(model)
table[:, :3].proxify.highlight_current(mode="all")
table.show()
```

or

```py
indexer = (slice(None), slice(None, 3))
proxy = custom_models.SliceFilterProxyModel(indexer=indexer)
proxy.set_source_model(model)
table.set_model(proxy)
table.show()
```

<figure markdown>
  ![Image title](../../images/highlightcurrentproxymodel_all.png)
  <figcaption>Mode: all</figcaption>
</figure>

<figure markdown>
  ![Image title](../../images/highlightcurrentproxymodel_column.png)
  <figcaption>Mode: column</figcaption>
</figure>

<figure markdown>
  ![Image title](../../images/highlightcurrentproxymodel_row.png)
  <figcaption>Mode: row</figcaption>
</figure>

### API

::: prettyqt.custom_models.SliceColorValuesProxyModel

### Qt Properties

| Qt Property         | Type                     | Description                        |
| --------------------|--------------------------| -----------------------------------|
| **highlight_mode**: | `str`                    | Highlighting mode                  |
| **highlight_color** | `gui.QColor`             | Color to use for highlighted cells |
| **highlight_role**  | `constants.ItemDataRole` | Role to use for comparing          |
