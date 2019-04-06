# -*- coding: utf-8 -*-

"""widgets module

contains QtWidgets-based classes
"""

from .application import Application

from .widget import Widget
from .graphicsitem import GraphicsItem
from .styleoption import StyleOption
from .dialog import Dialog
from .messagebox import MessageBox

from .formlayout import FormLayout
from .boxlayout import BoxLayout
from .gridlayout import GridLayout

from .slider import Slider
from .styleoptionslider import StyleOptionSlider

from .action import Action
from .toolbutton import ToolButton
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
from .filedialog import FileDialog
from .dialogbuttonbox import DialogButtonBox
from .groupbox import GroupBox
from .splitter import Splitter

from .mainwindow import MainWindow

from .itemdelegate import ItemDelegate

from .composed.spanslider import SpanSlider
from .composed.waitingspinner import WaitingSpinner
from .composed.callout import Callout
from .composed.markdownwidget import MarkdownWindow, MarkdownWidget
from .composed.image import Image
from .composed.imageviewer import ImageViewer
from .composed.popupinfo import PopupInfo
from .composed.buttondelegate import ButtonDelegate

__all__ = ["Application",
           "Widget",
           "GraphicsItem",
           "StyleOption",
           "Dialog",
           "MessageBox",
           "FormLayout",
           "BoxLayout",
           "GridLayout",
           "Slider",
           "StyleOptionSlider",
           "Action",
           "ToolButton",
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
           "FileDialog",
           "DialogButtonBox",
           "GroupBox",
           "Splitter",
           "MainWindow",
           "ItemDelegate",
           "SpanSlider",
           "WaitingSpinner",
           "Callout",
           "PopupInfo",
           "ButtonDelegate",
           "Image",
           "ImageViewer",
           "MarkdownWindow",
           "MarkdownWidget"]
