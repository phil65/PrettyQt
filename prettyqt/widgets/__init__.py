"""widgets module.

contains QtWidgets-based classes
"""

from __future__ import annotations

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

from .style import Style
from .commonstyle import CommonStyle
from .proxystyle import ProxyStyle
from .application import Application
from .sizepolicy import SizePolicy
from .widget import Widget
from .frame import Frame
from .focusframe import FocusFrame
from .abstractslider import AbstractSlider
from .abstractscrollarea import AbstractScrollArea
from .abstractbutton import AbstractButton
from .abstractspinbox import AbstractSpinBox
from .abstractitemview import AbstractItemView
from .scrollbar import ScrollBar
from .scrollarea import ScrollArea
from .rubberband import RubberBand
from .graphicstransform import GraphicsTransform
from .graphicsrotation import GraphicsRotation
from .graphicsscale import GraphicsScale
from .graphicsitem import GraphicsItem
from .graphicsitemgroup import GraphicsItemGroup
from .abstractgraphicsshapeitem import AbstractGraphicsShapeItem
from .graphicspixmapitem import GraphicsPixmapItem
from .graphicsobject import GraphicsObject
from .graphicstextitem import GraphicsTextItem
from .graphicslayoutitem import GraphicsLayoutItem
from .graphicslayout import GraphicsLayout
from .graphicsgridlayout import GraphicsGridLayout
from .graphicslinearlayout import GraphicsLinearLayout
from .graphicsanchorlayout import GraphicsAnchorLayout
from .graphicswidget import GraphicsWidget
from .graphicsproxywidget import GraphicsProxyWidget
from .graphicslineitem import GraphicsLineItem
from .graphicsrectitem import GraphicsRectItem
from .graphicssimpletextitem import GraphicsSimpleTextItem
from .graphicspolygonitem import GraphicsPolygonItem
from .graphicsellipseitem import GraphicsEllipseItem
from .graphicspathitem import GraphicsPathItem
from .graphicseffect import GraphicsEffect
from .graphicsblureffect import GraphicsBlurEffect
from .graphicscolorizeeffect import GraphicsColorizeEffect
from .graphicsdropshadoweffect import GraphicsDropShadowEffect
from .graphicsopacityeffect import GraphicsOpacityEffect
from .graphicsscene import GraphicsScene
from .graphicsview import GraphicsView
from .styleoption import StyleOption
from .styleoptionbutton import StyleOptionButton
from .styleoptioncomplex import StyleOptionComplex
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
from .pushbutton import PushButton
from .dialogbuttonbox import DialogButtonBox
from .dialog import Dialog
from .messagebox import MessageBox
from .errormessage import ErrorMessage

from .fileiconprovider import FileIconProvider
from .filesystemmodel import FileSystemModel

from .slider import Slider
from .dial import Dial

from .dockwidget import DockWidget

from .action import Action
from .actiongroup import ActionGroup
from .shortcut import Shortcut
from .undocommand import UndoCommand
from .undostack import UndoStack
from .undogroup import UndoGroup
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
from .combobox import ComboBox
from .fontcombobox import FontComboBox
from .spinbox import SpinBox
from .doublespinbox import DoubleSpinBox
from .checkbox import CheckBox
from .lineedit import LineEdit
from .keysequenceedit import KeySequenceEdit
from .textedit import TextEdit
from .datetimeedit import DateTimeEdit
from .dateedit import DateEdit
from .timeedit import TimeEdit
from .calendarwidget import CalendarWidget
from .plaintextedit import PlainTextEdit
from .textbrowser import TextBrowser
from .completer import Completer
from .progressbar import ProgressBar
from .lcdnumber import LCDNumber
from .columnview import ColumnView
from .listview import ListView
from .listwidget import ListWidget
from .treeview import TreeView
from .tablewidgetselectionrange import TableWidgetSelectionRange
from .treewidget import TreeWidget
from .treewidgetitemiterator import TreeWidgetItemIterator
from .tableview import TableView
from .tablewidgetitem import TableWidgetItem
from .tablewidget import TableWidget
from .scrollerproperties import ScrollerProperties
from .scroller import Scroller
from .abstractitemdelegate import AbstractItemDelegate
from .itemdelegate import ItemDelegate
from .styleditemdelegate import StyledItemDelegate
from .systemtrayicon import SystemTrayIcon

from .layoutitem import LayoutItem
from .widgetitem import WidgetItem
from .layout import Layout
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

from .gesture import Gesture
from .tapgesture import TapGesture
from .tapandholdgesture import TapAndHoldGesture
from .pangesture import PanGesture
from .pinchgesture import PinchGesture
from .swipegesture import SwipeGesture

from .itemeditorcreatorbase import ItemEditorCreatorBase
from .itemeditorfactory import ItemEditorFactory


def app(args: list[str] | None = None) -> Application:
    instance = Application.instance()
    if instance is not None:
        return instance
    Application.disable_window_help_button()
    return Application([] if args is None else args)


__all__ = [
    "app",
    "Application",
    "AbstractSlider",
    "AbstractButton",
    "AbstractSpinBox",
    "AbstractScrollArea",
    "AbstractItemView",
    "MdiSubWindow",
    "MdiArea",
    "ScrollBar",
    "ScrollArea",
    "Widget",
    "RubberBand",
    "GraphicsTransform",
    "GraphicsRotation",
    "GraphicsScale",
    "GraphicsItem",
    "GraphicsItemGroup",
    "AbstractGraphicsShapeItem",
    "GraphicsPixmapItem",
    "GraphicsObject",
    "GraphicsTextItem",
    "GraphicsLayoutItem",
    "GraphicsLayout",
    "GraphicsGridLayout",
    "GraphicsAnchorLayout",
    "GraphicsLinearLayout",
    "GraphicsWidget",
    "GraphicsProxyWidget",
    "GraphicsLineItem",
    "GraphicsRectItem",
    "GraphicsSimpleTextItem",
    "GraphicsPolygonItem",
    "GraphicsEllipseItem",
    "GraphicsPathItem",
    "GraphicsWidget",
    "GraphicsEffect",
    "GraphicsBlurEffect",
    "GraphicsDropShadowEffect",
    "GraphicsColorizeEffect",
    "GraphicsOpacityEffect",
    "GraphicsScene",
    "GraphicsView",
    "Style",
    "CommonStyle",
    "ProxyStyle",
    "StyleOption",
    "StyleOptionComplex",
    "SpacerItem",
    "SizePolicy",
    "StylePainter",
    "StyleFactory",
    "Dialog",
    "MessageBox",
    "ErrorMessage",
    "FileIconProvider",
    "FileSystemModel",
    "LayoutItem",
    "WidgetItem",
    "Layout",
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
    "FocusFrame",
    "ListWidgetItem",
    "TreeWidgetItem",
    "TreeWidgetItemIterator",
    "Action",
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
    "CommandLinkButton",
    "RadioButton",
    "ComboBox",
    "FontComboBox",
    "SpinBox",
    "DoubleSpinBox",
    "CheckBox",
    "LineEdit",
    "KeySequenceEdit",
    "TextEdit",
    "DateEdit",
    "TimeEdit",
    "DateTimeEdit",
    "CalendarWidget",
    "PlainTextEdit",
    "TextBrowser",
    "Completer",
    "ProgressBar",
    "LCDNumber",
    "ColumnView",
    "ListView",
    "ListWidget",
    "TreeView",
    "TreeWidget",
    "TableWidgetSelectionRange",
    "ScrollerProperties",
    "Scroller",
    "TableView",
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
    "ItemDelegate",
    "StyledItemDelegate",
    "SystemTrayIcon",
    "UndoCommand",
    "UndoStack",
    "UndoGroup",
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
    "TapGesture",
    "TapAndHoldGesture",
    "PanGesture",
    "PinchGesture",
    "SwipeGesture",
    "ItemEditorFactory",
    "ItemEditorCreatorBase",
]
