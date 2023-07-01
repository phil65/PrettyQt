
!!! note
    If you only need filtering based on slices or a single column / row,
    the SliceFilterProxymodel should be preferred for performance reasons.

### Example

```py
proxy = custom_models.SubsetFilterProxyModel()
proxy.set_source_model(model)
table.set_model(proxy)
table.show()
```

### API

::: prettyqt.custom_models.SubsetFilterProxyModel
