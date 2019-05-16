# -*- coding: utf-8 -*-

"""widgets module

contains QtWidgets-based classes
"""

from .application import Application
from .widget import Widget
from .frame import Frame
from .abstractslider import AbstractSlider
from .abstractscrollarea import AbstractScrollArea
from .abstractbutton import AbstractButton
from .abstractspinbox import AbstractSpinBox
from .abstractitemview import AbstractItemView
from .mdisubwindow import MdiSubWindow
from .mdiarea import MdiArea
from .scrollarea import ScrollArea
from .desktopwidget import DesktopWidget
from .graphicsitem import GraphicsItem
from .style import Style
from .styleoption import StyleOption
from .spaceritem import SpacerItem
from .sizepolicy import SizePolicy
from .stylepainter import StylePainter
from .dialog import BaseDialog, Dialog
from .messagebox import MessageBox
from .errormessage import ErrorMessage

from .filesystemmodel import FileSystemModel

from .slider import Slider
from .styleoptionslider import StyleOptionSlider


from .dockwidget import DockWidget

from .mainwindow import MainWindow

from .listwidgetitem import ListWidgetItem
from .action import Action
from .widgetaction import WidgetAction
from .toolbutton import ToolButton
from .tooltip import ToolTip
from .menu import Menu
from .menubar import MenuBar
from .statusbar import StatusBar
from .tabbar import TabBar
from .tabwidget import TabWidget
from .toolbar import ToolBar
from .headerview import HeaderView
from .label import Label
from .pushbutton import PushButton
from .commandlinkbutton import CommandLinkButton
from .radiobutton import RadioButton
from .combobox import ComboBox
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
from .progressbar import ProgressBar
from .listview import ListView
from .listwidget import ListWidget
from .treeview import TreeView
from .tableview import TableView
from .itemdelegate import ItemDelegate
from .styleditemdelegate import StyledItemDelegate

from .layout import Layout
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
from .dialogbuttonbox import DialogButtonBox
from .buttongroup import ButtonGroup
from .groupbox import GroupBox
from .splitter import Splitter
from .wizard import Wizard
from .wizardpage import WizardPage


def app():
    return Application.create_default_app()


__all__ = ["app",
           "Application",
           "AbstractSlider",
           "AbstractButton",
           "AbstractSpinBox",
           "AbstractScrollArea",
           "AbstractItemView",
           "MdiSubWindow",
           "MdiArea",
           "ScrollArea",
           "Widget",
           "DesktopWidget",
           "GraphicsItem",
           "Style",
           "StyleOption",
           "SpacerItem",
           "SizePolicy",
           "StylePainter",
           "BaseDialog",
           "Dialog",
           "MessageBox",
           "ErrorMessage",
           "FileSystemModel",
           "Layout",
           "FormLayout",
           "BoxLayout",
           "StackedLayout",
           "GridLayout",
           "ToolBox",
           "Slider",
           "StyleOptionSlider",
           "Frame",
           "ListWidgetItem",
           "Action",
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
           "ProgressBar",
           "ListView",
           "ListWidget",
           "TreeView",
           "TableView",
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
           "ItemDelegate",
           "StyledItemDelegate"]
