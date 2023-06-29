## MultiColumnFilterProxyModel

can take a seperate search term / value for each column, thus avoiding to layer proxy models in case you want to filter based on several columns. That way it is less demanding since filtering for all columns is done in one go.|
: Used by FilterHeader widget.

### Example

```py
    proxy = custom_models.MultiColumnFilterProxyModel()
    proxy.set_source_model(model)
    table.set_model(proxy)
    table.show()
```

### API

::: prettyqt.custom_models.MultiColumnFilterProxyModel
