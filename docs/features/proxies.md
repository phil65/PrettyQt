## Proxy Models

Every class containing the AbstractItemViewMixin (widgets.TreeView, widgets.TableView, ...)
has quick access to proxy superpowers hidden behind the "proxifier" attribute.
The following section will give an overview about the included proxies and how to apply them.


### Slice proxies

PrettyQt introduces a base proxy model which allows its subclasses to be selectively applied to
the source model by using python slicing syntax.
They can get quickly set up via our proxifier.


Example:

``` py
    model = MyTableModel()
    table = widgets.TableView()
    table.set_model(model)

    # lets change the appearance a bit.
    # Set the font color of column 2 and 3 to red and font to Courier.

    table.proxifier[2:4, :].style(foreground="red", font="Courier")

    # Cut off last column and only show last 50 lines.
    table.proxifier[:-1, :50].filter()

    # Set first 20 lines of these 50 lines to read_only
    table.proxifier[:, :20].change_flags(editable=False)

    # Make first column checkable and trigger callback on checkstate change.
    table.proxifier[0, :].make_checkable(callback=my_callback)
```

Every call here basically adds another ProxyModel layer (all based on SliceIdentityProxyModel).
The proxy models should all perform very well with large tables since they never need to loop over the whole column / row range.

The proxifier attribute basically gives quick access to set up these proxies.

``` py
    table.proxifier[:-1, 5::2].filter()
```
basically equals something like:

``` py
    proxy = SliceFilterProxyModel(indexer=(slice(None, -1, 1), slice(5, None, 2)))
    proxy.setSourceModel(table.model())
    table.set_model(proxy)
```

If you want to apply a slice proxy to the whole model, use slices without start and stop values:

``` py
    table.proxifier[:, :].style(background="green")
```

Here is a short overview of the included slice proxies:


`SliceAppearanceProxyModel`
: Applies styling to given slice by overriding font, color and alignment roles.

`SliceChangeFlagsProxyModel`
: Selectively change the result of the model.flags method. (Example: Change the IsEditable Flag to make an area read-only)

`SliceChangeIconSizeProxymodel`
: Allows to change the size of the Icon / Pixmap shown for DecorationRole.
Changed icons / pixmaps are cached for performance reasons.

`SliceChangeIconSizeProxymodel`
: Allows to change the size of the Icon / Pixmap shown for DecorationRole.
Changed icons / pixmaps are cached for performance reasons.

`SliceCheckableProxyModel`
: Makes an area of the table / tree checkable and triggers a callback on checkstate change.
  With keyword argument "tree=True", this model also works with trees and propagates changes to its children and parents
  to show the correct tristate.

`SliceColorValuesProxyModel`
: Color an area with numerical values based on their value (Example: high numbers red, low numbers green).
: To color cells, this proxy needs a minimum and maximum value. Three modes are available:
: Let the user choose a min max value.
: Use min max value from currently visible table section.
: use min max value from "seen" table content. (meaning that the model adapts min max values based.)

The last two modes have the advantage that nothing needs to be computed in advance, min/max values are calculated on-the fly.
`SliceFilterProxyModel`
: Show only selected slice of given source model.

`SliceValueTransformationProxyModel`
: Changes the values of any data role of given slice area based on a callback.


### Sort/Filter proxies.

In addition to the mentioned SliceFilterProxyModel, PrettyQt also contains
several proxies based on QSortFilterProxyModel. These can be more powerful
than the mentioned SliceFilterProxyModel, but scale with O(1) in respect to row / column count. (meaning that things might get slower for very large tables or when several proxies are layered on top of each other.)
Some of these proxies might partly overlap in functionality, but theres always a best one one for each use case to pick.


`FuzzyFilterProxyModel`
  : Model to make implementing CommandPalettes a la SubimeText or VS Code super easy.
  : A FilterProxyModel which sorts the results based on a matching score. Best matches are shown at the top.
  : Exposes matching score via a custom UserRole if desired.
  : Can also color the found Substring by converting the display role to an HTML representation when combined with our "HtmlItemDelegate", which allows to display HTML in ItemView cells.


`ValueFilterProxymodel`
: like the original QSortFilterProxyModel, but also works with non-str values.
: can be used for example to filter by checkstate role, or by any custom data behind any UserRole.
: The properties filterKeyColumn and filterRole of the base proxy model are taken into account.


`SubsetFilterProxyModel`
: Can filter rows / columns based on slices, index, a filter function, a list of indexes (like columns [0, 3, 7])

!!! note
    If you only need filtering based on slices or a single column / row,
    the SliceFilterProxymodel should be preferred for performance reasons.


`PredicateFilterProxyModel`
: The properties filterKeyColumn and filterRole of the base proxy model are taken into account.


`RangeFilterProxyModel`
: can filter a table based on min/max values of a numerical column.
: The properties filterKeyColumn and filterRole of the base proxy model are taken into account.


`MulticolumnFilterProxyModel`:
: can take a seperate search term / value for each column, thus avoiding to layer proxy models in case you want to filter based on several columns. That way it is less demanding since filtering for all columns is done in one go.
: Used by FilterHeader widget.


## Reshape proxies

`TableToListProxyModel`:
: Stack all columns into one single column
: To stack row-wise, use a TransposeProxyModel first.

`FlattenedTreeProxyModel`:
: Moves all rows up to the root level.
: Label can be changed to show the complete path.

`MeltProxyModel`:
: Unpivot a Table from wide to long format.
: same as pandas.melt, just without pandas.




## Other Proxies


`HighlightMouseProxymodel`
