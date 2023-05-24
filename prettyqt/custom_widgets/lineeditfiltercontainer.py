from __future__ import annotations

from prettyqt import constants, widgets


class LineEditFilterContainer(widgets.Widget):
    def __init__(self, parent: widgets.TableView | widgets.TreeView, **kwargs):
        super().__init__(**kwargs)
        self.set_layout("vertical")
        self._proxies = []
        self.searchbar = widgets.HBoxLayout(margin=0, spacing=1)
        model = parent.model()
        parent.h_header.sectionResized.connect(self._resize_lineedits)
        for i in range(parent.h_header.count()):
            lineedit = widgets.LineEdit()
            proxy = core.SortFilterProxyModel(self)
            self._proxies.append(proxy)
            proxy.setRecursiveFilteringEnabled(True)
            proxy.setSourceModel(model)
            proxy.setFilterKeyColumn(i)
            lineedit.set_margin(0)
            lineedit.value_changed.connect(proxy.setFilterFixedString)
            self.searchbar.add(lineedit)
            model = proxy
            lineedit.setFixedWidth(parent.h_header.sectionSize(i))
            title = model.headerData(i, constants.HORIZONTAL, constants.DISPLAY_ROLE)
            lineedit.setPlaceholderText(f"Filter {title}...")
        self.searchbar.addStretch()
        parent.set_model(model)
        self.box.add(self.searchbar)
        self.box.add(parent)

    def _resize_lineedits(self, index, old_size, new_size):
        # perhaps check header.sectionPosition() and sectionSize() for correct pos?
        self.searchbar[index].setFixedWidth(new_size)

    def setFilterCaseSensitivity(self, sensitivity):
        for proxy in self._proxies:
            proxy.setFilterCaseSensitivity(sensitivity)


if __name__ == "__main__":
    from prettyqt import core

    app = widgets.app()
    view = widgets.TreeView()
    view.setRootIsDecorated(True)
    model = widgets.FileSystemModel()
    model.set_root_path("/")
    model.setReadOnly(True)
    view.setModel(model)
    view.resize(640, 480)
    view.set_selection_behavior("rows")
    view.adapt_sizes()
    w = LineEditFilterContainer(view)
    w.show()
    with app.debug_mode():
        app.main_loop()
