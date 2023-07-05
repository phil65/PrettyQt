
```py
from prettyqt import custom_models, widgets

app = widgets.app()
widget = widgets.TreeView()
model = custom_models.SubClassTreeModel(core.AbstractItemModelMixin)
widget.set_model(model)
widget.show()
```

<figure markdown>
  ![Image title](abstractitemmodelmixin_subclasses.png)
</figure>

::: prettyqt.custom_models.SubClassTreeModel

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
