from __future__ import annotations

from prettyqt import core, widgets


class TwoListsSelectionWidget(widgets.Widget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = self.set_layout("horizontal")
        self.left_list = widgets.ListWidget()
        self.right_list = widgets.ListWidget()

        self.all_to_right_btn = widgets.PushButton(">>")
        self.to_right_btn = widgets.PushButton(">")
        self.to_left_btn = widgets.PushButton("<")
        self.all_to_left_btn = widgets.PushButton("<<")

        vlay = widgets.VBoxLayout()
        vlay.addStretch()
        vlay.add(self.all_to_right_btn)
        vlay.add(self.to_right_btn)
        vlay.add(self.to_left_btn)
        vlay.add(self.all_to_left_btn)
        vlay.addStretch()

        self.btn_up = widgets.PushButton("Up")
        self.btn_down = widgets.PushButton("Down")

        vlay2 = widgets.VBoxLayout()
        vlay2.addStretch()
        vlay2.add(self.btn_up)
        vlay2.add(self.btn_down)
        vlay2.addStretch()

        layout.add(self.left_list)
        layout.addLayout(vlay)
        layout.add(self.right_list)
        layout.addLayout(vlay2)

        self.update_buttons_status()
        self.left_list.itemSelectionChanged.connect(self.update_buttons_status)
        self.right_list.itemSelectionChanged.connect(self.update_buttons_status)
        self.to_right_btn.clicked.connect(self.on_to_right_btn_clicked)
        self.to_left_btn.clicked.connect(self.on_to_left_btn_clicked)
        self.all_to_left_btn.clicked.connect(self.on_all_to_left_btn_clicked)
        self.all_to_right_btn.clicked.connect(self.on_all_to_right_btn_clicked)
        self.btn_up.clicked.connect(self.on_up_btn_clicked)
        self.btn_down.clicked.connect(self.on_down_btn_clicked)

    @core.Slot()
    def update_buttons_status(self):
        self.btn_up.setDisabled(
            not bool(self.right_list.selectedItems()) or self.right_list.currentRow() == 0
        )
        self.btn_down.setDisabled(
            not bool(self.right_list.selectedItems())
            or self.right_list.currentRow() == (self.right_list.count() - 1)
        )
        self.to_right_btn.setDisabled(
            not bool(self.left_list.selectedItems()) or self.right_list.currentRow() == 0
        )
        self.to_left_btn.setDisabled(not bool(self.right_list.selectedItems()))

    @core.Slot()
    def on_to_right_btn_clicked(self):
        self.right_list.add_item(self.left_list.takeItem(self.left_list.currentRow()))

    @core.Slot()
    def on_to_left_btn_clicked(self):
        self.left_list.add_item(self.right_list.takeItem(self.right_list.currentRow()))

    @core.Slot()
    def on_all_to_left_btn_clicked(self):
        while self.right_list.count() > 0:
            self.left_list.add_item(self.right_list.takeItem(0))

    @core.Slot()
    def on_all_to_right_btn_clicked(self):
        while self.left_list.count() > 0:
            self.right_list.add_item(self.left_list.takeItem(0))

    @core.Slot()
    def on_up_btn_clicked(self):
        row = self.right_list.currentRow()
        current_item = self.right_list.takeItem(row)
        self.right_list.insertItem(row - 1, current_item)
        self.right_list.setCurrentRow(row - 1)

    @core.Slot()
    def on_down_btn_clicked(self):
        row = self.right_list.currentRow()
        current_item = self.right_list.takeItem(row)
        self.right_list.insertItem(row + 1, current_item)
        self.right_list.setCurrentRow(row + 1)

    def add_items_left(self, items):
        self.left_list.add_items(items)

    def get_left_elements(self):
        return [self.left_list.item(i) for i in range(self.left_list.count())]

    def get_right_elements(self):
        return [self.right_list.item(i) for i in range(self.right_list.count())]


if __name__ == "__main__":
    app = widgets.app()
    list_selection = TwoListsSelectionWidget()
    list_selection.add_items_left([f"item-{i}" for i in range(5)])

    def on_clicked_left():
        print(list_selection.get_left_elements())

    def on_clicked_right():
        print(list_selection.get_right_elements())

    l_button = widgets.PushButton(text="print left elements", clicked=on_clicked_left)
    r_button = widgets.PushButton(text="print right elements", clicked=on_clicked_right)
    w = widgets.Widget()
    lay = widgets.VBoxLayout(w)
    hlay = widgets.HBoxLayout()
    hlay.add(l_button)
    hlay.add(r_button)
    lay.addLayout(hlay)
    lay.add(list_selection)
    w.show()
    app.exec()
