# -*- coding: utf-8 -*-

"""widgets module.

contains QtWidgets-based classes
"""

from .style import Style
from .application import Application
from .sizepolicy import SizePolicy
from .widget import Widget
from .frame import Frame
from .abstractslider import AbstractSlider
from .abstractscrollarea import AbstractScrollArea
from .abstractbutton import AbstractButton
from .abstractspinbox import AbstractSpinBox
from .abstractitemview import AbstractItemView
from .scrollbar import ScrollBar
from .scrollarea import ScrollArea
from .desktopwidget import DesktopWidget
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
from .styleoptioncomplex import StyleOptionComplex
from .stylepainter import StylePainter
from .stylefactory import StyleFactory
from .pushbutton import PushButton
from .dialogbuttonbox import DialogButtonBox
from .dialog import BaseDialog, Dialog
from .messagebox import MessageBox
from .errormessage import ErrorMessage

from .filesystemmodel import FileSystemModel

from .slider import Slider
from .styleoptionslider import StyleOptionSlider
from .styleoptionframe import StyleOptionFrame

from .dockwidget import DockWidget
from .action import Action
from .actiongroup import ActionGroup
from .widgetaction import WidgetAction
from .menu import Menu
from .mainwindow import MainWindow

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
from .columnview import ColumnView
from .listview import ListView
from .listwidget import ListWidget
from .treeview import TreeView
from .treewidget import TreeWidget
from .tableview import TableView
from .tablewidgetitem import TableWidgetItem
from .tablewidget import TableWidget
from .abstractitemdelegate import AbstractItemDelegate
from .itemdelegate import ItemDelegate
from .styleditemdelegate import StyledItemDelegate
from .systemtrayicon import SystemTrayIcon

from .layoutitem import LayoutItem
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
from .splitter import Splitter
from .wizard import Wizard
from .wizardpage import WizardPage

from .undocommand import UndoCommand
from .undostack import UndoStack
from .undogroup import UndoGroup
from .undoview import UndoView

from .datawidgetmapper import DataWidgetMapper
from .sizegrip import SizeGrip

from .keyeventtransition import KeyEventTransition
from .mouseeventtransition import MouseEventTransition


def app():
    if Application.instance() is not None:
        return Application.instance()
    Application.disable_window_help_button()
    return Application([])


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
    "DesktopWidget",
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
    "StyleOption",
    "StyleOptionComplex",
    "SpacerItem",
    "SizePolicy",
    "StylePainter",
    "StyleFactory",
    "BaseDialog",
    "Dialog",
    "MessageBox",
    "ErrorMessage",
    "FileSystemModel",
    "LayoutItem",
    "Layout",
    "FormLayout",
    "BoxLayout",
    "StackedLayout",
    "GridLayout",
    "ToolBox",
    "Slider",
    "StyleOptionSlider",
    "StyleOptionFrame",
    "Frame",
    "ListWidgetItem",
    "TreeWidgetItem",
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
    "ColumnView",
    "ListView",
    "ListWidget",
    "TreeView",
    "TreeWidget",
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
    "Splitter",
    "Wizard",
    "WizardPage",
    "MainWindow",
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
]
