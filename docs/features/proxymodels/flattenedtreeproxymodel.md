## FlattenedTreeProxyModel

Proxy model to unpivot a table from wide to long format, as known from pandas.

### Example

```py
    app = widgets.app()
    data = dict(
        first=["John", "Mary"],
        last=["Doe", "Bo"],
        height=[5.5, 6.0],
        weight=[130, 150],
    )
    model = gui.StandardItemModel.from_dict(data)
    table = widgets.TableView()
    table.set_model(model)
    table.show()
```

<figure markdown>
  ![Image title](../../images/meltproxymodel_before.png)
  <figcaption>Original table</figcaption>
</figure>



```py
    table.proxifier.flatten()
    table.show()
```
or
```py
    proxy = custom_models.FlattenedTreeProxyModel()
    proxy.set_source_model(model)
    table.set_model(proxy)
    table.show()
```
<figure markdown>
  ![Image title](../../images/flattenedtreeproxymodel.png)
  <figcaption>FlattenedTreeProxyModel</figcaption>
</figure>

### API

::: prettyqt.custom_models.FlattenedTreeProxyModel

### Qt Properties

| Qt Property     | Type        | Description                             |
| ----------------|-------------| --------------------------------------- |
| **id_columns**: | `list[int]` | Columns to use as identifier variables  |
| **var_name**    | `str`       | Header for variable column              |
| **value_name**  | `str`       | Header for value column                 |
