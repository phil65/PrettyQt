## FilterHeader

HeaderView subclass which includes LineEdits / Dropdowns with filter possibilities.
When setting the header view on an ItemView, a proxy model will be created which is linked to the filter widgets.
The correct filter widget is automatically inferred from the content of the columns.

```py
    model = MyModel()
    widget = widgets.TableView()
    widget.set_model(model)
    widget.h_header = custom_widgets.FilterHeader() # same as setHorizontalHeader()
```

<figure markdown>
  ![Image title](../../images/filterheader.png)
  <figcaption>FilterHeader widget</figcaption>
</figure>
