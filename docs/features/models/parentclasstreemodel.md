!!! Example "Class hierarchy example"

    === "Parentclass tree"

        ```py
        from prettyqt import itemmodels, widgets

        app = widgets.app()
        widget = widgets.TreeView()
        model = itemmodels.ParentClassTreeModel(widgets.TreeWidget)
        widget.set_model(model)
        widget.show()
        ```

        <figure markdown>
          ![Image title](treewidget_parentclasses.png)
        </figure>

    === "MRO tree"

        ```py
        from prettyqt import itemmodels, widgets

        app = widgets.app()
        widget = widgets.TreeView()
        model = itemmodels.ParentClassTreeModel(widgets.TreeWidget, mro=True)
        widget.set_model(model)
        widget.show()
        ```

        <figure markdown>
          ![Image title](treewidget_mro.png)
        </figure>


::: prettyqt.itemmodels.ParentClassTreeModel

## Supports

`type`

### Additional roles

| Role                                    | Data                       |
| ----------------------------------------|----------------------------|
| `ParentClassTreeModel.Roles.SourceRole` | Source code of the class   |
