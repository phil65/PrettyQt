Every class containing the AbstractItemViewMixin (`widgets.TreeView`, `widgets.TableView`, ...)
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

table.proxifier[:, 2:4].style(foreground="red", font="Courier")

# Cut off last column and only show last 50 lines.
table.proxifier[:50, :-1].filter()

# Set first 20 lines of these 50 lines to read_only
table.proxifier[:20, :].change_flags(editable=False)

# Make first column checkable and trigger callback on checkstate change.
table.proxifier[0].make_checkable(callback=my_callback)
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

| Proxy                                                                  | Description                                              |
| -----------------------------------------------------------------------|----------------------------------------------------------|
|[SliceAppearanceProxyModel](sliceappearanceproxymodel.md)                  | Applies styling to given slice by overriding font, color and alignment roles.|
|[SliceChangeFlagsProxyModel](slicechangeflagsproxymodel.md)                | Selectively change the ItemFlags of the model|
|[SliceChangeIconSizeProxymodel](slicechangeiconsizeproxymodel.md)          | Allows to change the size of the Icon / Pixmap shown for DecorationRole.|
|[SliceCheckableProxyModel](slicecheckableproxymodel.md)                    | Makes an area of the table checkable and triggers a callback on checkstate change.|
|[SliceCheckableTreeProxyModel](slicecheckabletreeproxymodel.md)            | Makes an area of a tree checkable and triggers a callback on checkstate change.|
|[SliceColorValuesProxyModel](slicecolorvaluesproxymodel.md)                | Color an area with numerical values based on their value.|
|[SliceFilterProxyModel](slicefilterproxymodel.md)                          | Show only selected slice of given source model.|
|[SliceValueTransformationProxyModel](slicevaluetransformationproxymodel.md)| Changes the values of any data role of given slice area based on a callback.|


### Sort/Filter proxies.

In addition to the mentioned SliceFilterProxyModel, PrettyQt also contains
several proxies based on QSortFilterProxyModel. These can be more powerful
than the mentioned SliceFilterProxyModel, but scale with O(1) in respect to row / column count. (meaning that things might get slower for very large tables or when several proxies are layered on top of each other.)
Some of these proxies might partly overlap in functionality, but theres always a best one one for each use case to pick.

| Proxy                                            | Description                                              |
| -------------------------------------------------|----------------------------------------------------------|
|[FuzzyFilterProxyModel](fuzzyfilterproxymodel.md) |Model for implementing a CommandPalette a la SubimeText.  |
|[ValueFilterProxymodel](valuefilterproxymodel.md)         |Similar to QSortFilterProxyModel, but also works with non-str values.|
|[SubsetFilterProxyModel](subsetfilterproxymodel.md)        |Filter based on slices, index, a filter function, a list of indexes (like columns [0, 3, 7])
|[PredicateFilterProxyModel](predicatefilterproxymodel.md)     |Filter based on predicates.|
|[RangeFilterProxyModel](rangefilterproxymodel.md)         |Filter based on min/max values of a numerical column.|
|[MulticolumnFilterProxyModel](multicolumnfilterproxymodel.md)   | can take a seperate search term / value for each column.|


## Reshape proxies

| Proxy                                                | Description                              |
| -----------------------------------------------------|------------------------------------------|
|[TableToListProxyModel](tabletolistproxymodel.md)     | Stack all columns into one single column |
|[FlattenedTreeProxyModel](flattenedtreeproxymodel.md) | Moves all rows up to the root level.     |
|[MeltProxyModel](meltproxymodel.md)                   |Unpivot a Table from wide to long format. |
|[ColumnOrderProxyModel](columnorderproxymodel.md)     |Reorder columns and hide columns.         |


## Other Proxies

| Proxy                                                  | Description                                          |
| -------------------------------------------------------|------------------------------------------------------|
|[ChangeHeadersProxyModel](changeheadersproxymodel.md)   | Change horizontal / vertical headers.                |
|[HighlightMouseProxymodel](highlightmouseproxymodel.md) | Highlight regions the mouse cursor is hovering over. |



## Tools

`ProxyMapper`

When having a complex proxy tree like:

``` mermaid
classDiagram
  Shared_proxy <|-- Proxy_1_1
  Shared_proxy <|-- Proxy_2_1
  Proxy_1_1 <|-- Proxy_1_2
  Proxy_2_1 <|-- Proxy_2_2
  Root_model <-- Shared_proxy
  class Proxy_1_1{
  }
  class Proxy_2_1{
  }
  class Root_model{
  }
```

then the ProxyMapper can be used to map indexes and ItemSelections easily between any of the proxies.

``` py
    mapper = ProxyMapper(proxy_1_2, proxy_2_1)
    index = proxy_1_2.index(0, 0)
    mapped_index = mapper.map_index_from_one_to_two(index)
```

The mapper will find the closest parent ("shared_proxy" here),
use mapToSource / mapSelectionFromSource until it gets there,
and then use mapFromSource / mapSelectionFromSource to get down to 2_1.
