# -*- coding: utf-8 -*-

"""widgets module

contains QtWidgets-based classes
"""

from .formlayout import FormLayout
from .image import Image

from .slider import Slider
from .styleoptionslider import StyleOptionSlider
from .spanslider import SpanSlider

from .menu import Menu
from .tabwidget import TabWidget
from .toolbar import Toolbar
from .headerview import HeaderView
from .dockwidget import DockWidget
from .pushbutton import PushButton

from .splashscreen import SplashScreen
from .filedialog import FileDialog
from .imageviewer import ImageViewer
from .dialogbuttonbox import DialogButtonBox

from .mainwindow import MainWindow

from .composed.waitingspinner import WaitingSpinner
from .composed.callout import Callout
from .popupinfo import PopupInfo
from .buttondelegate import ButtonDelegate

__all__ = ["FormLayout",
           "Image",
           "Slider",
           "StyleOptionSlider",
           "SpanSlider",
           "Menu",
           "TabWidget",
           "Toolbar",
           "HeaderView",
           "DockWidget",
           "PushButton",
           "SplashScreen",
           "FileDialog",
           "ImageViewer",
           "DialogButtonBox",
           "MainWindow",
           "WaitingSpinner",
           "Callout",
           "PopupInfo",
           "ButtonDelegate"]
