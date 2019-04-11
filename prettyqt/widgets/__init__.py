# -*- coding: utf-8 -*-

"""widgets module

contains QtWidgets-based classes
"""

from .application import Application

from .widget import Widget
from .desktopwidget import DesktopWidget
from .graphicsitem import GraphicsItem
from .style import Style
from .styleoption import StyleOption
from .sizepolicy import SizePolicy
from .stylepainter import StylePainter
from .dialog import Dialog
from .messagebox import MessageBox

from .formlayout import FormLayout
from .boxlayout import BoxLayout
from .gridlayout import GridLayout

from .slider import Slider
from .styleoptionslider import StyleOptionSlider
from .frame import Frame

from .action import Action
from .widgetaction import WidgetAction
from .toolbutton import ToolButton
from .tooltip import ToolTip
from .menu import Menu
from .menubar import MenuBar
from .statusbar import StatusBar
from .tabbar import TabBar
from .tabwidget import TabWidget
from .toolbar import Toolbar
from .headerview import HeaderView
from .dockwidget import DockWidget
from .label import Label
from .pushbutton import PushButton
from .radiobutton import RadioButton
from .combobox import ComboBox
from .spinbox import SpinBox
from .doublespinbox import DoubleSpinBox
from .checkbox import CheckBox
from .lineedit import LineEdit
from .textedit import TextEdit
from .plaintextedit import PlainTextEdit
from .textbrowser import TextBrowser
from .progressbar import ProgressBar
from .treeview import TreeView
from .tableview import TableView

from .splashscreen import SplashScreen
from .progressdialog import ProgressDialog
from .fontdialog import FontDialog
from .filedialog import FileDialog
from .dialogbuttonbox import DialogButtonBox
from .buttongroup import ButtonGroup
from .groupbox import GroupBox
from .splitter import Splitter

from .mainwindow import MainWindow

from .itemdelegate import ItemDelegate

from .composed.spanslider import SpanSlider
from .composed.waitingspinner import WaitingSpinner
from .composed.callout import Callout
from .composed.markdownwidget import MarkdownWindow
from .composed.imageviewer import ImageViewer
from .composed.popupinfo import PopupInfo
from .composed.buttondelegate import ButtonDelegate
from .composed.selectionwidget import SelectionWidget

__all__ = ["Application",
           "Widget",
           "DesktopWidget",
           "GraphicsItem",
           "Style",
           "StyleOption",
           "SizePolicy",
           "StylePainter",
           "Dialog",
           "MessageBox",
           "FormLayout",
           "BoxLayout",
           "GridLayout",
           "Slider",
           "StyleOptionSlider",
           "Frame",
           "Action",
           "WidgetAction",
           "ToolButton",
           "ToolTip",
           "Menu",
           "MenuBar",
           "StatusBar",
           "TabWidget",
           "TabBar",
           "Toolbar",
           "HeaderView",
           "DockWidget",
           "Label",
           "PushButton",
           "RadioButton",
           "ComboBox",
           "SpinBox",
           "DoubleSpinBox",
           "CheckBox",
           "LineEdit",
           "TextEdit",
           "PlainTextEdit",
           "TextBrowser",
           "ProgressBar",
           "TreeView",
           "TableView",
           "SplashScreen",
           "ProgressDialog",
           "FontDialog",
           "FileDialog",
           "DialogButtonBox",
           "ButtonGroup",
           "GroupBox",
           "Splitter",
           "MainWindow",
           "ItemDelegate",
           "SpanSlider",
           "WaitingSpinner",
           "Callout",
           "PopupInfo",
           "ButtonDelegate",
           "SelectionWidget",
           "Image",
           "ImageViewer",
           "MarkdownWindow"]
