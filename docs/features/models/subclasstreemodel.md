
```py
from prettyqt import itemmodels, widgets

app = widgets.app()
widget = widgets.TreeView()
model = itemmodels.SubClassTreeModel(core.AbstractItemModelMixin)
widget.set_model(model)
widget.show()
```

<figure markdown>
  ![Image title](abstractitemmodelmixin_subclasses.png)
</figure>

::: prettyqt.itemmodels.SubClassTreeModel

## Supports

`type` | `types.UnionType`

### Additional roles

| Role                                 | Data                       |
| -------------------------------------|----------------------------|
| `SubClassTreeModel.Roles.SourceRole` | Source code of the class   |


### Qt Properties

| Qt Property  | Type    | Description                                                     |
| -------------|---------|-----------------------------------------------------------------|
| **show_mro** | `bool`  | List complete mro as children instead of just direct subclasses |
