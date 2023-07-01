## ModelIndexModel

Tree model to display a a list of ModelIndexes from another model.
Displayed role columns can either be the Qt default roles or roles fetched from QAbstractItemModel.roleNames()

### API

::: prettyqt.custom_models.ModelIndexModel

## Supports

`list[core.QModelIndex]`


## Example

```py
# get indexes from some random model
model_for_indexes = ParentClassTreeModel(widgets.QWidget, show_mro=True)
model_for_indexes.prefetch_tree()
indexes = list(test.iter_tree())
model = ModelIndexModel(indexes=indexes)
```

### Qt Properties

| Qt Property          | Type     | Description                                     |
| ---------------------|----------|-------------------------------------------------|
| **use_model_roles**: | `bool`   | Use QAbstractItemModel.roleNames() for columns  |
