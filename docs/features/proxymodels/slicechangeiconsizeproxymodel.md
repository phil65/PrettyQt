::: prettyqt.custom_models.SliceChangeIconSizeProxyModel


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


### Qt Properties

| Qt Property         | Type        | Description                  |
| --------------------|-------------| ---------------------------- |
| **column_slice**    | `slice`     | Slice for filtering columns  |
| **row_slice**       | `slice`     | Slice for filtering rows     |
| **icon_size**       | `core.QSize`| Icon size for DecorationRole |

!!! note
    Due to Qt limitations, the Qt properties contain a list with 3 items instead of a slice.
