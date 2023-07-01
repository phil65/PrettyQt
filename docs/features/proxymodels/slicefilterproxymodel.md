Proxy model to filter an item view based on python slicing syntax.
Since slicing operations are bijective, this model can filter without
looping through rows or columns. Thus, this should perform much better than a
SortFilterProxyModel with a column filter. (O(1) instead of O(n))

### Example

To filter out every second row, and cut off the the first two columns:

```py
model = MyModel()
table = widgets.TableView()
table.set_model(model)
table.proxifier[::2, 2:].filter()
table.show()
```

or

```py
indexer = (slice(None, None, 2), slice(2, None))
proxy = custom_models.SliceFilterProxyModel(indexer=indexer)
proxy.set_source_model(model)
table.set_model(proxy)
table.show()
```

Read more about [slices](https://docs.python.org/3/library/functions.html#slice).

### API

::: prettyqt.custom_models.SliceFilterProxyModel

### Qt Properties

| Qt Property      | Type     | Description                  |
| -----------------|----------| ---------------------------- |
| **column_slice** | `slice`  | Slice for filtering columns  |
| **row_slice**:   | `slice`  | Slice for filtering rows     |

!!! note
    Due to Qt limitations, the Qt properties contain a list with 3 items instead of a slice.
