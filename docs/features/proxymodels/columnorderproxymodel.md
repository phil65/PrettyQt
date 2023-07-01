Proxy model which reorders the columns the source model by passing a list containing the new order. If not all indexes are part of the list, then the
missing sections will be hidden.

### Example

```py
table.proxifier.reorder_columns(order=[3, 2, 0])
table.show()
```
or

```py
model = MyModel()
proxy = ColumnOrderProxyModel(order=[3, 2, 0])
proxy.set_source_model(model)
table.set_model(proxy)
table.show()
```

### API

::: prettyqt.custom_models.ColumnOrderProxyModel

### Qt Properties

| Qt Property         | Type                     | Description                        |
| --------------------|--------------------------| -----------------------------------|
| **highlight_mode**: | `str`                    | Highlighting mode                  |
