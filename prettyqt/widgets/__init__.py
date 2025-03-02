"""Classes to extend Qt GUI with widgets."""

from __future__ import annotations

import sys

from prettyqt.qt.QtWidgets import *  # noqa: F403

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
from .lineedit import LineEdit
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
from .label import Label
from .toolbar import ToolBar
from .headerview import HeaderView
from .commandlinkbutton import CommandLinkButton
from .radiobutton import RadioButton
from .combobox import ComboBox, ComboBoxMixin
from .fontcombobox import FontComboBox
from .spinbox import SpinBox
from .doublespinbox import DoubleSpinBox
from .checkbox import CheckBox
from .keysequenceedit import KeySequenceEdit
from .textedit import TextEdit, TextEditMixin
from .datetimeedit import DateTimeEdit, DateTimeEditMixin
from .dateedit import DateEdit
from .timeedit import TimeEdit
from .calendarwidget import CalendarWidget
from .plaintextedit import PlainTextEdit, PlainTextEditMixin
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
from .hboxlayout import HBoxLayout
from .vboxlayout import VBoxLayout
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


# to register delegates
from prettyqt import validators
from prettyqt import itemdelegates
from prettyqt import custom_widgets
from prettyqt import itemmodels
from prettyqt.qt import QtWidgets

QT_MODULE = QtWidgets


def app(args: list[str] | None = None, style: str = "Fusion", **kwargs) -> Application:
    if (instance := Application.instance()) is not None:
        return instance
    #  + ["--ignore-gpu-blacklist", "--enable-gpu-rasterization"]
    app = Application(sys.argv if args is None else args, **kwargs)
    app.set_style(style)
    return app


__all__ = [
    "AbstractButton",
    "AbstractButtonMixin",
    "AbstractGraphicsShapeItem",
    "AbstractGraphicsShapeItemMixin",
    "AbstractItemDelegate",
    "AbstractItemDelegateMixin",
    "AbstractItemView",
    "AbstractItemViewMixin",
    "AbstractScrollArea",
    "AbstractScrollAreaMixin",
    "AbstractSlider",
    "AbstractSliderMixin",
    "AbstractSpinBox",
    "AbstractSpinBoxMixin",
    "Application",
    "BoxLayout",
    "ButtonGroup",
    "CalendarWidget",
    "CheckBox",
    "ColorDialog",
    "ColumnView",
    "ComboBox",
    "ComboBoxMixin",
    "CommandLinkButton",
    "CommonStyle",
    "CommonStyleMixin",
    "Completer",
    "DataWidgetMapper",
    "DateEdit",
    "DateTimeEdit",
    "DateTimeEditMixin",
    "Dial",
    "Dialog",
    "DialogButtonBox",
    "DialogMixin",
    "DockWidget",
    "DoubleSpinBox",
    "ErrorMessage",
    "FileDialog",
    "FileIconProvider",
    "FileSystemModel",
    "FocusFrame",
    "FontComboBox",
    "FontDialog",
    "FormLayout",
    "Frame",
    "FrameMixin",
    "Gesture",
    "GestureMixin",
    "GraphicsAnchorLayout",
    "GraphicsBlurEffect",
    "GraphicsColorizeEffect",
    "GraphicsDropShadowEffect",
    "GraphicsEffect",
    "GraphicsEffectMixin",
    "GraphicsEllipseItem",
    "GraphicsGridLayout",
    "GraphicsItem",
    "GraphicsItemGroup",
    "GraphicsItemMixin",
    "GraphicsLayout",
    "GraphicsLayoutItem",
    "GraphicsLayoutItemMixin",
    "GraphicsLayoutMixin",
    "GraphicsLineItem",
    "GraphicsLinearLayout",
    "GraphicsObject",
    "GraphicsObjectMixin",
    "GraphicsOpacityEffect",
    "GraphicsPathItem",
    "GraphicsPixmapItem",
    "GraphicsPolygonItem",
    "GraphicsProxyWidget",
    "GraphicsRectItem",
    "GraphicsRotation",
    "GraphicsScale",
    "GraphicsScene",
    "GraphicsSimpleTextItem",
    "GraphicsTextItem",
    "GraphicsTransform",
    "GraphicsTransformMixin",
    "GraphicsView",
    "GraphicsViewMixin",
    "GraphicsWidget",
    "GraphicsWidget",
    "GraphicsWidgetMixin",
    "GridLayout",
    "GroupBox",
    "HBoxLayout",
    "HeaderView",
    "InputDialog",
    "ItemDelegate",
    "ItemEditorCreatorBase",
    "ItemEditorFactory",
    "KeySequenceEdit",
    "LCDNumber",
    "Label",
    "Layout",
    "LayoutItem",
    "LayoutItemMixin",
    "LayoutMixin",
    "LineEdit",
    "ListView",
    "ListViewMixin",
    "ListWidget",
    "ListWidgetItem",
    "MainWindow",
    "MdiArea",
    "MdiSubWindow",
    "Menu",
    "MenuBar",
    "MessageBox",
    "PanGesture",
    "PinchGesture",
    # "KeyEventTransition",
    # "MouseEventTransition",
    # "GraphicsSceneHoverEvent",
    # "GraphicsSceneMouseEvent",
    # "GraphicsSceneWheelEvent",
    # "GraphicsSceneContextMenuEvent",
    # "GraphicsSceneDragDropEvent",
    # "GraphicsSceneHelpEvent",
    # "GraphicsSceneMoveEvent",
    # "GraphicsSceneResizeEvent",
    # "GraphicsSceneEvent",
    # "GestureEvent",
    "PlainTextDocumentLayout",
    "PlainTextEdit",
    "PlainTextEditMixin",
    "ProgressBar",
    "ProgressDialog",
    "ProxyStyle",
    "PushButton",
    "PushButtonMixin",
    "RadioButton",
    "RubberBand",
    "ScrollArea",
    "ScrollBar",
    "Scroller",
    "ScrollerProperties",
    "SizeGrip",
    "SizePolicy",
    "Slider",
    "SpacerItem",
    "SpinBox",
    "SplashScreen",
    "Splitter",
    "SplitterHandle",
    "StackedLayout",
    "StackedWidget",
    "StatusBar",
    "Style",
    "StyleFactory",
    "StyleMixin",
    "StyleOption",
    "StyleOptionButton",
    "StyleOptionComboBox",
    "StyleOptionComplex",
    "StyleOptionComplexMixin",
    "StyleOptionDockWidget",
    "StyleOptionFocusRect",
    "StyleOptionFrame",
    "StyleOptionGraphicsItem",
    "StyleOptionGroupBox",
    "StyleOptionHeader",
    "StyleOptionMenuItem",
    "StyleOptionMixin",
    "StyleOptionProgressBar",
    "StyleOptionRubberBand",
    "StyleOptionSizeGrip",
    "StyleOptionSlider",
    "StyleOptionSpinBox",
    "StyleOptionTab",
    "StyleOptionTabBarBase",
    "StyleOptionTabWidgetFrame",
    "StyleOptionTitleBar",
    "StyleOptionToolBar",
    "StyleOptionToolBox",
    "StyleOptionToolButton",
    "StyleOptionViewItem",
    "StylePainter",
    "StyledItemDelegate",
    "SwipeGesture",
    "SystemTrayIcon",
    "TabBar",
    "TabWidget",
    "TableView",
    "TableViewMixin",
    "TableWidget",
    "TableWidgetItem",
    "TableWidgetSelectionRange",
    "TapAndHoldGesture",
    "TapGesture",
    "TextBrowser",
    "TextEdit",
    "TextEditMixin",
    "TimeEdit",
    "ToolBar",
    "ToolBox",
    "ToolButton",
    "ToolTip",
    "TreeView",
    "TreeViewMixin",
    "TreeWidget",
    "TreeWidgetItem",
    "TreeWidgetItemIterator",
    "UndoView",
    "VBoxLayout",
    "WhatsThis",
    "Widget",
    "WidgetAction",
    "WidgetItem",
    "WidgetMixin",
    "Wizard",
    "WizardPage",
    "app",
    "custom_widgets",
    "itemdelegates",
    "itemmodels",
    "validators",
]
