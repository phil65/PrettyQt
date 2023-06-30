## FuzzyFilterProxyModel

A FilterProxyModel which sorts the results based on a matching score. Best matches are shown at the top.
Exposes matching score via a custom UserRole if desired.
The proxy can also color the found Substring by converting the display role to an HTML representation when combined with our [HtmlItemDelegate][htmlitemdelegate], which allows to display HTML in ItemView cells.

### Example

```py
proxy = custom_models.FuzzyFilterProxyModel()
proxy.set_source_model(model)
table.set_model(proxy)
table.show()
```

### API

::: prettyqt.custom_models.FuzzyFilterProxyModel
