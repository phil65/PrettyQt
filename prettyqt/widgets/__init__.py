# -*- coding: utf-8 -*-

"""widgets module

contains QtWidgets-based classes
"""

from .widget import Widget
from .formlayout import FormLayout

from .slider import Slider
from .styleoptionslider import StyleOptionSlider

from .action import Action
from .menu import Menu
from .tabbar import TabBar
from .tabwidget import TabWidget
from .toolbar import Toolbar
from .headerview import HeaderView
from .dockwidget import DockWidget
from .label import Label
from .pushbutton import PushButton
from .radiobutton import RadioButton
from .combobox import ComboBox
from .textedit import TextEdit
from .plaintextedit import PlainTextEdit

from .splashscreen import SplashScreen
from .progressdialog import ProgressDialog
from .filedialog import FileDialog
from .dialogbuttonbox import DialogButtonBox

from .mainwindow import MainWindow

from .composed.spanslider import SpanSlider
from .composed.waitingspinner import WaitingSpinner
from .composed.callout import Callout
from .composed.markdownwidget import MarkdownWindow, MarkdownWidget
from .composed.image import Image
from .composed.imageviewer import ImageViewer
from .composed.popupinfo import PopupInfo
from .composed.buttondelegate import ButtonDelegate

__all__ = ["Widget",
           "FormLayout",
           "Slider",
           "StyleOptionSlider",
           "SpanSlider",
           "Action",
           "Menu",
           "TabWidget",
           "TabBar",
           "Toolbar",
           "HeaderView",
           "DockWidget",
           "Label",
           "PushButton",
           "RadioButton",
           "ComboBox",
           "TextEdit",
           "PlainTextEdit",
           "SplashScreen",
           "ProgressDialog",
           "FileDialog",
           "ImageViewer",
           "DialogButtonBox",
           "MainWindow",
           "WaitingSpinner",
           "Callout",
           "PopupInfo",
           "ButtonDelegate",
           "Image",
           "MarkdownWindow",
           "MarkdownWidget"]
