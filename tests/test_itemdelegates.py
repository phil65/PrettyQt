"""Tests for `prettyqt` package."""

import enum

from prettyqt import constants, core, gui, itemdelegates, widgets
from prettyqt.qt import QtCore


def test_buttondelegate(qtbot):
    table = widgets.TableView()
    widget = itemdelegates.ButtonDelegate(parent=table)
    widget.setEditorData(widgets.Widget(), None)
    widget.createEditor(None, None, QtCore.QModelIndex())
    # widget.currentIndexChanged()


def test_radiodelegate(qtbot, tablewidget):
    delegate = itemdelegates.RadioDelegate(tablewidget, ["a", "b"])
    tablewidget.show()
    tablewidget.setItemDelegateForColumn(0, delegate)
    tablewidget.openPersistentEditor(tablewidget[0, 0])
    tablewidget.hide()


def test_icondelegate(qtbot, tablewidget):
    delegate = itemdelegates.IconDelegate()
    tablewidget.show()
    tablewidget.setItemDelegateForColumn(0, delegate)
    tablewidget.hide()


def test_nofocusdelegate(qtbot, tablewidget):
    delegate = itemdelegates.NoFocusDelegate()
    tablewidget.show()
    tablewidget.setItemDelegateForColumn(0, delegate)
    tablewidget.hide()


def test_stardelegate(qtbot, tablewidget):
    delegate = itemdelegates.StarDelegate()
    tablewidget.show()
    tablewidget.setItemDelegateForColumn(0, delegate)
    tablewidget.hide()


def test_progressbardelegate(qtbot, tablewidget):
    delegate = itemdelegates.ProgressBarDelegate()
    tablewidget.show()
    tablewidget.setItemDelegateForColumn(0, delegate)
    tablewidget.hide()


def test_editordelegate(qtbot, tablewidget):
    delegate = itemdelegates.EditorDelegate(parent=tablewidget)
    tablewidget.show()
    tablewidget.setItemDelegateForColumn(0, delegate)
    tablewidget.hide()


def test_widgetdelegate(qtbot, tablewidget):
    delegate = itemdelegates.WidgetDelegate(parent=tablewidget)
    tablewidget.show()
    tablewidget.setItemDelegateForColumn(0, delegate)
    tablewidget.hide()
    assert delegate._editor_for_index(core.ModelIndex()) is None
    editor = widgets.Widget()
    opt = widgets.StyleOptionViewItem()
    opt.rect = core.QRect(10, 20, 100, 30)
    delegate.updateEditorGeometry(editor, opt, core.ModelIndex())
    assert editor.geometry() == opt.rect


def test_icondelegate_paint_types(qtbot):
    model = gui.StandardItemModel(4, 1)
    pm = gui.QPixmap(16, 16)
    pm.fill(gui.QColor("red"))
    img = gui.QImage(16, 16, gui.QImage.Format.Format_ARGB32)
    img.fill(gui.QColor("blue"))
    model.setData(model.index(0, 0), pm, constants.USER_ROLE)
    model.setData(model.index(1, 0), img, constants.USER_ROLE)
    model.setData(model.index(2, 0), gui.QColor("green"), constants.USER_ROLE)
    model.setData(model.index(3, 0), gui.QIcon(pm), constants.USER_ROLE)

    delegate = itemdelegates.IconDelegate()
    canvas = gui.QPixmap(100, 40)
    with gui.Painter(canvas) as painter:
        for row in range(4):
            opt = widgets.StyleOptionViewItem()
            opt.rect = core.QRect(0, 0, 100, 40)
            opt.decorationSize = core.QSize(16, 16)
            delegate.paint(painter, opt, model.index(row, 0))


def test_progressbardelegate_none_and_total(qtbot):
    model = gui.StandardItemModel(2, 1)
    model.setData(model.index(0, 0), None, constants.DISPLAY_ROLE)
    model.setData(model.index(1, 0), 50, constants.DISPLAY_ROLE)
    delegate = itemdelegates.ProgressBarDelegate(total=200)
    canvas = gui.QPixmap(100, 40)
    with gui.Painter(canvas) as painter:
        opt = widgets.StyleOptionViewItem()
        opt.rect = core.QRect(0, 0, 100, 40)
        delegate.paint(painter, opt, model.index(0, 0))
        delegate.paint(painter, opt, model.index(1, 0))


def test_stardelegate_none_and_star_at_position(qtbot):
    model = gui.StandardItemModel(2, 1)
    model.setData(model.index(0, 0), None, constants.DISPLAY_ROLE)
    model.setData(model.index(1, 0), 3, constants.DISPLAY_ROLE)
    delegate = itemdelegates.StarDelegate()
    canvas = gui.QPixmap(120, 40)
    with gui.Painter(canvas) as painter:
        opt = widgets.StyleOptionViewItem()
        opt.rect = core.QRect(0, 0, 120, 40)
        delegate.paint(painter, opt, model.index(0, 0))
        delegate.paint(painter, opt, model.index(1, 0))
    assert delegate.sizeHint(widgets.StyleOptionViewItem(), model.index(0, 0)).isValid()
    editor = itemdelegates.stardelegate.StarEditor()
    delegate.setEditorData(editor, model.index(0, 0))
    assert editor.star_rating.star_count == 0
    pos_star = editor.star_at_position(25.0)
    assert isinstance(pos_star, int)
    assert pos_star == 2  # noqa: PLR2004


def test_renderlinkdelegate_hover_flag(qtbot):
    model = gui.StandardItemModel(1, 1)
    model.setData(model.index(0, 0), "https://example.com", constants.DISPLAY_ROLE)
    delegate = itemdelegates.RenderLinkDelegate()
    canvas = gui.QPixmap(200, 40)
    with gui.Painter(canvas) as painter:
        opt = widgets.StyleOptionViewItem()
        opt.rect = core.QRect(0, 0, 200, 40)
        opt.state = widgets.Style.StateFlag.State_Enabled
        delegate.paint(painter, opt, model.index(0, 0))
        assert not painter.font().underline()
        opt.state |= widgets.Style.StateFlag.State_MouseOver
        delegate.paint(painter, opt, model.index(0, 0))


def test_buttondelegate_cell_entered_and_none_text(qtbot):
    table = widgets.TableView()
    model = gui.StandardItemModel(2, 1)
    model.setData(model.index(0, 0), None, constants.DISPLAY_ROLE)
    model.setData(model.index(0, 0), lambda: None, constants.USER_ROLE)
    model.setData(model.index(1, 0), "Click", constants.DISPLAY_ROLE)
    model.setData(model.index(1, 0), lambda: None, constants.USER_ROLE)
    table.setModel(model)
    delegate = itemdelegates.ButtonDelegate(parent=table)
    table.setItemDelegateForColumn(0, delegate)
    editor = delegate.createEditor(
        table, widgets.StyleOptionViewItem(), model.index(0, 0)
    )
    assert isinstance(editor, widgets.PushButton)
    assert editor.text() == ""
    delegate.cell_entered(model.index(0, 0))
    assert table.isPersistentEditorOpen(model.index(0, 0))
    delegate.cell_entered(model.index(1, 0))
    assert not table.isPersistentEditorOpen(model.index(0, 0))
    assert table.isPersistentEditorOpen(model.index(1, 0))


def test_editordelegate_enum_and_icon_no_widget(qtbot):
    class _Color(enum.Enum):
        RED = 1

    model = gui.StandardItemModel(2, 1)
    pm = gui.QPixmap(16, 16)
    pm.fill(gui.QColor("red"))
    model.setData(model.index(0, 0), gui.QIcon(pm), constants.EDIT_ROLE)
    model.setData(model.index(1, 0), _Color.RED, constants.EDIT_ROLE)
    delegate = itemdelegates.EditorDelegate(role=constants.EDIT_ROLE)
    canvas = gui.QPixmap(100, 40)
    with gui.Painter(canvas) as painter:
        opt = widgets.StyleOptionViewItem()
        opt.rect = core.QRect(0, 0, 100, 40)
        opt.decorationSize = core.QSize(16, 16)
        delegate.paint(painter, opt, model.index(0, 0))
        delegate.paint(painter, opt, model.index(1, 0))


def test_htmlitemdelegate_no_widget(qtbot):
    model = gui.StandardItemModel(1, 1)
    model.setData(model.index(0, 0), "<b>Hello</b>", constants.DISPLAY_ROLE)
    delegate = itemdelegates.HtmlItemDelegate()
    canvas = gui.QPixmap(120, 40)
    with gui.Painter(canvas) as painter:
        opt = widgets.StyleOptionViewItem()
        opt.rect = core.QRect(0, 0, 120, 40)
        delegate.paint(painter, opt, model.index(0, 0))


def test_radiodelegate_edit_role_and_focus_out_none_mask(qtbot, tablewidget):
    delegate = itemdelegates.RadioDelegate(tablewidget, ["a", "b"])
    model = tablewidget.model()
    idx = model.index(0, 0)
    editor = delegate.createEditor(tablewidget, widgets.StyleOptionViewItem(), idx)
    editor.button_group.button(1).setChecked(True)
    delegate.setModelData(editor, model, idx)
    assert model.data(idx, constants.EDIT_ROLE) == "b"

    # FocusOut when offMask is None must not raise
    dummy = widgets.Widget()
    ev = gui.QFocusEvent(core.Event.Type.FocusOut)
    delegate.eventFilter(dummy, ev)
