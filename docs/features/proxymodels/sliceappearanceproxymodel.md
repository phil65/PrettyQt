::: prettyqt.custom_models.SliceAppearanceProxyModel

### Qt Properties

| Qt Property          | Type               | Description                  |
| ---------------------|--------------------| ---------------------------- |
| **column_slice**     | `slice`            | Slice for filtering columns  |
| **row_slice**        | `slice`            | Slice for filtering rows     |
| **font_value**       | `QFont`            | Font to use                  |
| **foreground_value** | `QColor`, `QBrush` | Foreground to use            |
| **background_value** | `QColor`, `QBrush` | Background to use            |
| **alignment_value**  | 'AlignmentFlag'    | Alignment to use             |

!!! note
    Due to Qt limitations, slice properties contain a list with 3 items instead of a slice.
