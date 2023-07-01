Proxy model for changing the header data (either horizontal or vertical).

Header data can either be changed by passing a list with same length as source length or by passing a dictionary with index as key and new value as value (Example: {1: "abc", 3: "def"} changes section 1 to "abc" and section 3 to "def")
Apart from the regular use case of changing the text, the other roles can be changed to.

### Example

```py
table.proxifier.change_headers(header=["x", "y", "z"], orientation=constants.HORIZONTAL, role=constants.DISPLAY_ROLE)
table.show()
```
or

```py
model = MyModel()
proxy = ChangeHeadersProxyModel(header=["x", "y", "z"], orientation=constants.VERTICAL)
proxy.set_source_model(model)
table.set_model(proxy)
table.show()
```

### API

::: prettyqt.custom_models.ChangeHeadersProxyModel

### Qt Properties

| Qt Property  | Type            | Description                  |
| -------------|-----------------|------------------------------|
| **header**   | `dict` or `list`| Default font for whole table |
