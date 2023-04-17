"""widgets module.

contains QtWidgets-based classes
"""

from __future__ import annotations

import sys

from prettyqt.qt.QtWidgets import (
    QGraphicsSceneHoverEvent as GraphicsSceneHoverEvent,
    QGraphicsSceneMouseEvent as GraphicsSceneMouseEvent,
    QGraphicsSceneWheelEvent as GraphicsSceneWheelEvent,
    QGraphicsSceneContextMenuEvent as GraphicsSceneContextMenuEvent,
    QGraphicsSceneDragDropEvent as GraphicsSceneDragDropEvent,
    QGraphicsSceneHelpEvent as GraphicsSceneHelpEvent,
    QGraphicsSceneMoveEvent as GraphicsSceneMoveEvent,
    QGraphicsSceneResizeEvent as GraphicsSceneResizeEvent,
    QGraphicsSceneEvent as GraphicsSceneEvent,
    QGestureEvent as GestureEvent,
)

from .style import Style, StyleMixin
from .commonstyle import CommonStyle, CommonStyleMixin
from .proxystyle import ProxyStyle
from .application import Application
from .sizepolicy import SizePolicy
from .widget import Widget, WidgetMixin
from .frame import Frame, FrameMixin
from .focusframe import FocusFrame
from .abstractslider import AbstractSlider, AbstractSliderMixin
from .abstractscrollarea import AbstractScrollArea, AbstractScrollAreaMixin
from .abstractbutton import AbstractButton, AbstractButtonMixin
from .abstractspinbox import AbstractSpinBox, AbstractSpinBoxMixin
from .abstractitemview import AbstractItemView, AbstractItemViewMixin
from .scrollbar import ScrollBar
from .scrollarea import ScrollArea
from .rubberband import RubberBand
from .graphicstransform import GraphicsTransform, GraphicsTransformMixin
from .graphicsrotation import GraphicsRotation
from .graphicsscale import GraphicsScale
from .graphicsitem import GraphicsItem, GraphicsItemMixin
from .graphicsitemgroup import GraphicsItemGroup
from .abstractgraphicsshapeitem import (
    AbstractGraphicsShapeItem,
    AbstractGraphicsShapeItemMixin,
)
from .graphicspixmapitem import GraphicsPixmapItem
from .graphicsobject import GraphicsObject, GraphicsObjectMixin
from .graphicstextitem import GraphicsTextItem
from .graphicslayoutitem import GraphicsLayoutItem, GraphicsLayoutItemMixin
from .graphicslayout import GraphicsLayout, GraphicsLayoutMixin
from .graphicsgridlayout import GraphicsGridLayout
from .graphicslinearlayout import GraphicsLinearLayout
from .graphicsanchorlayout import GraphicsAnchorLayout
from .graphicswidget import GraphicsWidget, GraphicsWidgetMixin
from .graphicsproxywidget import GraphicsProxyWidget
from .graphicslineitem import GraphicsLineItem
from .graphicsrectitem import GraphicsRectItem
from .graphicssimpletextitem import GraphicsSimpleTextItem
from .graphicspolygonitem import GraphicsPolygonItem
from .graphicsellipseitem import GraphicsEllipseItem
from .graphicspathitem import GraphicsPathItem
from .graphicseffect import GraphicsEffect, GraphicsEffectMixin
from .graphicsblureffect import GraphicsBlurEffect
from .graphicscolorizeeffect import GraphicsColorizeEffect
from .graphicsdropshadoweffect import GraphicsDropShadowEffect
from .graphicsopacityeffect import GraphicsOpacityEffect
from .graphicsscene import GraphicsScene
from .graphicsview import GraphicsView, GraphicsViewMixin
from .styleoption import StyleOption, StyleOptionMixin
from .styleoptionbutton import StyleOptionButton
from .styleoptioncomplex import StyleOptionComplex, StyleOptionComplexMixin
from .styleoptiondockwidget import StyleOptionDockWidget
from .styleoptionfocusrect import StyleOptionFocusRect
from .styleoptionframe import StyleOptionFrame
from .styleoptiongraphicsitem import StyleOptionGraphicsItem
from .styleoptionheader import StyleOptionHeader
from .styleoptionmenuitem import StyleOptionMenuItem
from .styleoptionprogressbar import StyleOptionProgressBar
from .styleoptionrubberband import StyleOptionRubberBand
from .styleoptiontab import StyleOptionTab
from .styleoptiontabbarbase import StyleOptionTabBarBase
from .styleoptiontabwidgetframe import StyleOptionTabWidgetFrame
from .styleoptiontoolbar import StyleOptionToolBar
from .styleoptiontoolbox import StyleOptionToolBox
from .styleoptionviewitem import StyleOptionViewItem

from .styleoptioncombobox import StyleOptionComboBox
from .styleoptiongroupbox import StyleOptionGroupBox
from .styleoptionsizegrip import StyleOptionSizeGrip
from .styleoptionslider import StyleOptionSlider
from .styleoptionspinbox import StyleOptionSpinBox
from .styleoptiontitlebar import StyleOptionTitleBar
from .styleoptiontoolbutton import StyleOptionToolButton

from .stylepainter import StylePainter
from .stylefactory import StyleFactory
from .pushbutton import PushButton, PushButtonMixin
from .dialogbuttonbox import DialogButtonBox
from .dialog import Dialog, DialogMixin
from .messagebox import MessageBox
from .errormessage import ErrorMessage

from .fileiconprovider import FileIconProvider
from .filesystemmodel import FileSystemModel

from .slider import Slider
from .dial import Dial

from .dockwidget import DockWidget

from .action import Action, ActionMixin
from .actiongroup import ActionGroup
from .shortcut import Shortcut
from .widgetaction import WidgetAction
from .menu import Menu
from .mainwindow import MainWindow
from .whatsthis import WhatsThis
from .listwidgetitem import ListWidgetItem
from .treewidgetitem import TreeWidgetItem
from .toolbutton import ToolButton
from .tooltip import ToolTip
from .menubar import MenuBar
from .statusbar import StatusBar
from .tabbar import TabBar
from .tabwidget import TabWidget
from .mdisubwindow import MdiSubWindow
from .mdiarea import MdiArea
from .toolbar import ToolBar
from .headerview import HeaderView
from .label import Label
from .commandlinkbutton import CommandLinkButton
from .radiobutton import RadioButton
from .combobox import ComboBox, ComboBoxMixin
from .fontcombobox import FontComboBox
from .spinbox import SpinBox
from .doublespinbox import DoubleSpinBox
from .checkbox import CheckBox
from .lineedit import LineEdit
from .keysequenceedit import KeySequenceEdit
from .textedit import TextEdit, TextEditMixin
from .datetimeedit import DateTimeEdit, DateTimeEditMixin
from .dateedit import DateEdit
from .timeedit import TimeEdit
from .calendarwidget import CalendarWidget
from .plaintextedit import PlainTextEdit
from .textbrowser import TextBrowser
from .completer import Completer
from .progressbar import ProgressBar
from .lcdnumber import LCDNumber
from .columnview import ColumnView
from .listview import ListView, ListViewMixin
from .listwidget import ListWidget
from .treeview import TreeView, TreeViewMixin
from .tablewidgetselectionrange import TableWidgetSelectionRange
from .treewidget import TreeWidget
from .treewidgetitemiterator import TreeWidgetItemIterator
from .tableview import TableView, TableViewMixin
from .tablewidgetitem import TableWidgetItem
from .tablewidget import TableWidget
from .scrollerproperties import ScrollerProperties
from .scroller import Scroller
from .abstractitemdelegate import AbstractItemDelegate, AbstractItemDelegateMixin
from .itemdelegate import ItemDelegate
from .styleditemdelegate import StyledItemDelegate
from .systemtrayicon import SystemTrayIcon

from .layoutitem import LayoutItem, LayoutItemMixin
from .widgetitem import WidgetItem
from .layout import Layout, LayoutMixin
from .spaceritem import SpacerItem
from .formlayout import FormLayout
from .boxlayout import BoxLayout
from .stackedlayout import StackedLayout
from .gridlayout import GridLayout
from .toolbox import ToolBox

from .splashscreen import SplashScreen
from .progressdialog import ProgressDialog
from .fontdialog import FontDialog
from .filedialog import FileDialog
from .colordialog import ColorDialog
from .inputdialog import InputDialog
from .buttongroup import ButtonGroup
from .groupbox import GroupBox
from .splitterhandle import SplitterHandle
from .splitter import Splitter
from .wizard import Wizard
from .wizardpage import WizardPage
from .stackedwidget import StackedWidget

from .undoview import UndoView

from .datawidgetmapper import DataWidgetMapper
from .sizegrip import SizeGrip

from .plaintextdocumentlayout import PlainTextDocumentLayout

from .gesture import Gesture, GestureMixin
from .tapgesture import TapGesture
from .tapandholdgesture import TapAndHoldGesture
from .pangesture import PanGesture
from .pinchgesture import PinchGesture
from .swipegesture import SwipeGesture

from .itemeditorcreatorbase import ItemEditorCreatorBase
from .itemeditorfactory import ItemEditorFactory


def app(args: list[str] | None = None) -> Application:
    if (instance := Application.instance()) is not None:
        return instance
    Application.disable_window_help_button()
    return Application(sys.argv if args is None else args)


__all__ = [
    "app",
    "Application",
    "AbstractSlider",
    "AbstractSliderMixin",
    "AbstractButton",
    "AbstractButtonMixin",
    "AbstractSpinBox",
    "AbstractSpinBoxMixin",
    "AbstractScrollArea",
    "AbstractScrollAreaMixin",
    "AbstractItemView",
    "AbstractItemViewMixin",
    "MdiSubWindow",
    "MdiArea",
    "ScrollBar",
    "ScrollArea",
    "Widget",
    "WidgetMixin",
    "RubberBand",
    "GraphicsTransform",
    "GraphicsTransformMixin",
    "GraphicsRotation",
    "GraphicsScale",
    "GraphicsItem",
    "GraphicsItemMixin",
    "GraphicsItemGroup",
    "AbstractGraphicsShapeItem",
    "AbstractGraphicsShapeItemMixin",
    "GraphicsPixmapItem",
    "GraphicsObject",
    "GraphicsObjectMixin",
    "GraphicsTextItem",
    "GraphicsLayoutItem",
    "GraphicsLayoutItemMixin",
    "GraphicsLayout",
    "GraphicsLayoutMixin",
    "GraphicsGridLayout",
    "GraphicsAnchorLayout",
    "GraphicsLinearLayout",
    "GraphicsWidget",
    "GraphicsWidgetMixin",
    "GraphicsProxyWidget",
    "GraphicsLineItem",
    "GraphicsRectItem",
    "GraphicsSimpleTextItem",
    "GraphicsPolygonItem",
    "GraphicsEllipseItem",
    "GraphicsPathItem",
    "GraphicsWidget",
    "GraphicsEffect",
    "GraphicsEffectMixin",
    "GraphicsBlurEffect",
    "GraphicsDropShadowEffect",
    "GraphicsColorizeEffect",
    "GraphicsOpacityEffect",
    "GraphicsScene",
    "GraphicsView",
    "GraphicsViewMixin",
    "Style",
    "StyleMixin",
    "CommonStyle",
    "CommonStyleMixin",
    "ProxyStyle",
    "StyleOption",
    "StyleOptionMixin",
    "StyleOptionComplex",
    "StyleOptionComplexMixin",
    "SpacerItem",
    "SizePolicy",
    "StylePainter",
    "StyleFactory",
    "Dialog",
    "DialogMixin",
    "MessageBox",
    "ErrorMessage",
    "FileIconProvider",
    "FileSystemModel",
    "LayoutItem",
    "LayoutItemMixin",
    "WidgetItem",
    "Layout",
    "LayoutMixin",
    "FormLayout",
    "BoxLayout",
    "StackedLayout",
    "GridLayout",
    "ToolBox",
    "Slider",
    "Dial",
    "StyleOptionButton",
    "StyleOptionDockWidget",
    "StyleOptionFocusRect",
    "StyleOptionGraphicsItem",
    "StyleOptionHeader",
    "StyleOptionMenuItem",
    "StyleOptionProgressBar",
    "StyleOptionRubberBand",
    "StyleOptionTab",
    "StyleOptionTabBarBase",
    "StyleOptionTabWidgetFrame",
    "StyleOptionToolBar",
    "StyleOptionToolBox",
    "StyleOptionViewItem",
    "StyleOptionComboBox",
    "StyleOptionGroupBox",
    "StyleOptionSizeGrip",
    "StyleOptionSlider",
    "StyleOptionSpinBox",
    "StyleOptionTitleBar",
    "StyleOptionToolButton",
    "StyleOptionFrame",
    "Frame",
    "FrameMixin",
    "FocusFrame",
    "ListWidgetItem",
    "TreeWidgetItem",
    "TreeWidgetItemIterator",
    "Action",
    "ActionMixin",
    "ActionGroup",
    "WidgetAction",
    "ToolButton",
    "ToolTip",
    "Menu",
    "MenuBar",
    "StatusBar",
    "TabWidget",
    "TabBar",
    "ToolBar",
    "HeaderView",
    "DockWidget",
    "Label",
    "PushButton",
    "PushButtonMixin",
    "CommandLinkButton",
    "RadioButton",
    "ComboBox",
    "ComboBoxMixin",
    "FontComboBox",
    "SpinBox",
    "DoubleSpinBox",
    "CheckBox",
    "LineEdit",
    "KeySequenceEdit",
    "TextEdit",
    "TextEditMixin",
    "DateEdit",
    "TimeEdit",
    "DateTimeEdit",
    "DateTimeEditMixin",
    "CalendarWidget",
    "PlainTextEdit",
    "TextBrowser",
    "Completer",
    "ProgressBar",
    "LCDNumber",
    "ColumnView",
    "ListView",
    "ListViewMixin",
    "ListWidget",
    "TreeView",
    "TreeViewMixin",
    "TreeWidget",
    "TableWidgetSelectionRange",
    "ScrollerProperties",
    "Scroller",
    "TableView",
    "TableViewMixin",
    "TableWidgetItem",
    "TableWidget",
    "SplashScreen",
    "ProgressDialog",
    "FontDialog",
    "FileDialog",
    "ColorDialog",
    "InputDialog",
    "DialogButtonBox",
    "ButtonGroup",
    "GroupBox",
    "SplitterHandle",
    "Splitter",
    "Wizard",
    "WizardPage",
    "StackedWidget",
    "MainWindow",
    "Shortcut",
    "WhatsThis",
    "AbstractItemDelegate",
    "AbstractItemDelegateMixin",
    "ItemDelegate",
    "StyledItemDelegate",
    "SystemTrayIcon",
    "UndoView",
    "DataWidgetMapper",
    "SizeGrip",
    "KeyEventTransition",
    "MouseEventTransition",
    "GraphicsSceneHoverEvent",
    "GraphicsSceneMouseEvent",
    "GraphicsSceneWheelEvent",
    "GraphicsSceneContextMenuEvent",
    "GraphicsSceneDragDropEvent",
    "GraphicsSceneHelpEvent",
    "GraphicsSceneMoveEvent",
    "GraphicsSceneResizeEvent",
    "GraphicsSceneEvent",
    "GestureEvent",
    "PlainTextDocumentLayout",
    "Gesture",
    "GestureMixin",
    "TapGesture",
    "TapAndHoldGesture",
    "PanGesture",
    "PinchGesture",
    "SwipeGesture",
    "ItemEditorFactory",
    "ItemEditorCreatorBase",
]
