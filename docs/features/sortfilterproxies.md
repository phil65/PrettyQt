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
