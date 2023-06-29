## MultiColumnFilterProxyModel

This proxy uses seperate search term / values for each column in order to filter the source model, thus avoiding to layer proxy models in case you want to filter based on several columns. That way it is less demanding since filtering for all columns is done in one go.
This model is used by the [FilterHeader][filterheader] widget.

### Example

```py
    proxy = custom_models.MultiColumnFilterProxyModel()
    proxy.set_source_model(model)
    table.set_model(proxy)
    table.show()
```

### API

::: prettyqt.custom_models.MultiColumnFilterProxyModel
