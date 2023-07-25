Every class containing the AbstractItemViewMixin (`widgets.TreeView`, `widgets.TableView`, ...)
has quick access to proxy superpowers hidden behind the "[proxifier](proxifier.md)" attribute.
The following section will give an overview about the included proxies and how to apply them.


## Slice proxies

PrettyQt introduces a base proxy model which allows its subclasses to be selectively applied to
the source model by using python slicing syntax.
They can get quickly set up via our [Proxifier](proxifier.md).


Example:

```py
model = MyTableModel()
table = widgets.TableView()
table.set_model(model)

# lets change the appearance a bit.
# Set the font color of column 2 and 3 to red and font to Courier.

table.proxifier[:, 2:4].style(foreground="red", font="Courier")

# Cut off last column and only show last 50 lines.
table.proxifier[:50, :-1].filter()

# Set first 20 lines of these 50 lines to read_only
table.proxifier[:20, :].change_flags(editable=False)

# Make first column checkable and trigger callback on checkstate change.
table.proxifier[0].make_checkable(callback=my_callback)
```

Every call here basically adds another ProxyModel layer (all based on [SliceIdentityProxyModel](sliceidentityproxymodel.md)).
The proxy models should all perform very well with large tables since they never need to loop over the whole column / row range.

The proxifier attribute basically gives quick access to set up these proxies.

```py
table.proxifier[:-1, 5::2].filter()
```
basically equals something like:

```py
proxy = SliceFilterProxyModel(indexer=(slice(None, -1, 1), slice(5, None, 2)))
proxy.setSourceModel(table.model())
table.set_model(proxy)
```

If you want to apply a slice proxy to all cells of the model, use slices without start and stop values:

```py
table.proxifier[:, :].style(background="green")
```

Here is a short overview of the included slice proxies:

| Proxy                                                                  | Description                                              |
| -----------------------------------------------------------------------|----------------------------------------------------------|
|[SliceFilterProxyModel](slicefilterproxymodel.md)                          | Show only selected slice of given source model.|
|[SliceAppearanceProxyModel](sliceappearanceproxymodel.md)                  | Applies styling to given slice by overriding font, color and alignment roles.|
|[SliceChangeFlagsProxyModel](slicechangeflagsproxymodel.md)                | Selectively change the ItemFlags of the model|
|[SliceChangeIconSizeProxymodel](slicechangeiconsizeproxymodel.md)          | Allows to change the size of the Icon / Pixmap shown for DecorationRole.|
|[SliceCheckableProxyModel](slicecheckableproxymodel.md)                    | Makes an area of the table checkable and triggers a callback on checkstate change.|
|[SliceCheckableTreeProxyModel](slicecheckabletreeproxymodel.md)            | Makes an area of a tree checkable and triggers a callback on checkstate change.|
|[SliceColorValuesProxyModel](slicecolorvaluesproxymodel.md)                | Color an area with numerical values based on their value.|
|[SliceDisplayTextProxyModel](slicedisplaytextproxymodel.md)                | Format non-str DisplayRole values according to formatter strings.|
|[SliceMapRoleProxyModel](slicemaproleproxymodel.md)                        | Map an ItemDataRole to another.|
|[SliceValueTransformationProxyModel](slicevaluetransformationproxymodel.md)| Changes the values of any data role of given slice area based on a callback.|


## Sort/Filter proxies.

In addition to the mentioned SliceFilterProxyModel, PrettyQt also contains
several proxies based on QSortFilterProxyModel. These can be more powerful
than the mentioned [SliceFilterProxyModel](slicefilterproxymodel.md), but scale with O(1) in respect to row / column count. (meaning that things might get slower for very large tables or when several proxies are layered on top of each other.)
Some of these proxies might partly overlap in functionality, but theres always a best one one for each use case to pick.

| Proxy                                            | Description                                              |
| -------------------------------------------------|----------------------------------------------------------|
|[FuzzyFilterProxyModel](fuzzyfilterproxymodel.md) |Model for implementing a CommandPalette a la SubimeText.  |
|[ValueFilterProxymodel](valuefilterproxymodel.md)         |Similar to QSortFilterProxyModel, but also works with non-str values.|
|[SubsetFilterProxyModel](subsetfilterproxymodel.md)        |Filter based on slices, index, a filter function, a list of indexes (like columns [0, 3, 7])
|[PredicateFilterProxyModel](predicatefilterproxymodel.md)     |Filter based on predicates.|
|[RangeFilterProxyModel](rangefilterproxymodel.md)         |Filter based on min/max values of a numerical column.|
|[MulticolumnFilterProxyModel](multicolumnfilterproxymodel.md)   | can take a seperate search term / value for each column.|
                      |

## Reshape / Styling proxies


| Proxy                                                | Description                              |
| -----------------------------------------------------|------------------------------------------|
|[TableToListProxyModel](tabletolistproxymodel.md)     | Stack all columns into one single column |
|[FlattenTreeProxyModel](flattentreeproxymodel.md) | Moves all rows up to the root level.     |
|[MeltProxyModel](meltproxymodel.md)                   |Unpivot a Table from wide to long format. |
|[ColumnOrderProxyModel](columnorderproxymodel.md)     |Reorder columns and hide columns.         |
|[ChangeHeadersProxyModel](changeheadersproxymodel.md) | Change horizontal / vertical headers.    |
|[AppearanceProxyModel](appearanceproxymodel.md)       | Proxy model to change styling.           |



## Other Proxies

| Proxy                                                  | Description                                          |
| -------------------------------------------------------|------------------------------------------------------|
|[HighlightMouseProxymodel](highlightmouseproxymodel.md) | Highlight regions the mouse cursor is hovering over. |



## Miscellaneous

| Class                  | Description                                                                            |
| -----------------------|----------------------------------------------------------------------------------------|
| [ProxyMapper](proxymapper.md)          | A helper for mapping indexes between proxies in any proxy tree.                        |
| [LinkedSelectionModel](linkedselectionmodel.md) | A SelectionModel which keeps indexes of any amount of proxies / source models in sync. |
| [ProxyComparerWidget](proxycomparerwidget.md)  | A widget to compare a proxy chain, useful for debugging.                               |
