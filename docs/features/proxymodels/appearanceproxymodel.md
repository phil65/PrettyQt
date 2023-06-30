## AppearanceProxyModel

Proxy model for changing the "style roles" of the source model.

In contrast to [SliceAppearanceProxyModel][sliceappearanceproxymodel], this one works in a more "static" way, meaning that you can change the color / font / alignment of indexes via model.setData even when the source model is not item-based (like a StandardItemModel).


### Example

```py
model = MyModel()
proxy = custom_models.AppearanceProxyModel()
proxy.set_source_model(model)
proxy.setData(proxy.index(0, 0), gui.QColor("red"), role=constants.FOREGROUND_ROLE)
table.set_model(proxy)
table.show()
```

### API

::: prettyqt.custom_models.AppearanceProxyModel

### Qt Properties

| Qt Property            | Type                 | Description                         |
| -----------------------|----------------------|-------------------------------------|
| **font_default**:      | `QFont`              | Default font for whole table        |
| **foreground_default** | `QColor` or `QBrush` | Default foureground for whole table |
| **background_default** | `QColor` or `QBrush` | Default background for whole table  |
| **alignment_default**  | `AlignmentFlag`      | Default alignment for whole table   |
