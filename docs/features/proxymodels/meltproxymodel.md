
!!! Example "MeltProxyModel"

    === "Without proxy"

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
        # table.proxifier.melt(id_columns=[0, 1])
        table.show()

        ```
        <figure markdown>
          ![Image title](../../images/meltproxymodel_before.png)
        </figure>

    === "With proxy"

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
        table.proxifier.melt(id_columns=[0, 1])
        table.show()
        ```
        <figure markdown>
          ![Image title](../../images/meltproxymodel_after.png)
        </figure>

::: prettyqt.custom_models.MeltProxyModel


```py
table.proxifier.melt(id_columns=[0, 1])
# equals
proxy = custom_models.MeltProxyModel(id_columns=[0, 1])
proxy.set_source_model(table.model())
table.set_model(proxy)
```

### Qt Properties

| Qt Property     | Type        | Description                             |
| ----------------|-------------| --------------------------------------- |
| **id_columns**  | `list[int]` | Columns to use as identifier variables  |
| **var_name**    | `str`       | Header for variable column              |
| **value_name**  | `str`       | Header for value column                 |
