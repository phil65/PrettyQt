## ColumnJoinerProxyModel

Proxy model which joins the contents of several columns based on a formatter and appends it as a new column.

Example: When using a formatter "{0} - {1}: {4}", then the resulting column will show {Text of column 0} - {Text of Column 1}: {Text of Column 4}

### Example

```py
table.proxifier.join_columns(formatter="{0} - {2}", header="New column")
table.show()
```
or

```py
model = MyModel()
proxy = ColumnJoinerProxyModel()
proxy.set_source_model(model)
proxy.add_column(formatter="{0} - {2}", header="New column")
proxy.add_column(formatter="{4}: {5}", header="Another column")
table.set_model(proxy)
table.show()
```

### API

::: prettyqt.custom_models.ColumnJoinerProxyModel
