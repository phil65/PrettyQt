## SliceHighlightCurrentProxyModel

This proxy can be used to highlight all cells which contain the same content as the currently focused cell.
Three modes are possible:

| Mode    | Description                                                |
|---------|------------------------------------------------------------|
| all     | Highlights all cells with same content.                    |
| column  | Highlights all cells of the same column with same content. |
| row     | Highlights all cells of the same row with same content.    |


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

::: prettyqt.custom_models.SliceHighlightCurrentProxyModel

### Qt Properties

| Qt Property         | Type                     | Description                        |
| --------------------|--------------------------| -----------------------------------|
| **highlight_mode**: | `str`                    | Highlighting mode                  |
| **highlight_color** | `gui.QColor`             | Color to use for highlighted cells |
| **highlight_role**  | `constants.ItemDataRole` | Role to use for comparing          |
