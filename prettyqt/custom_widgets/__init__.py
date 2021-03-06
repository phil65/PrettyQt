"""Module containing custom widget classes."""

from prettyqt import core

from .image import Image
from .listinput import ListInput
from .booldicttoolbutton import BoolDictToolButton
from .optionalwidget import OptionalWidget
from .collapsibleframe import CollapsibleFrame
from .expandableline import ExpandableLine
from .singlelinetextedit import SingleLineTextEdit
from .regexinput import RegexInput
from .mappedcheckbox import MappedCheckBox
from .logtextedit import LogTextEdit
from .flagselectionwidget import FlagSelectionWidget
from .stringornumberwidget import StringOrNumberWidget
from .iconlabel import IconLabel
from .iconwidget import IconWidget
from .flowlayout import FlowLayout
from .borderlayout import BorderLayout
from .sidebarwidget import SidebarWidget
from .colorchooserbutton import ColorChooserButton
from .filechooserbutton import FileChooserButton
from .fontchooserbutton import FontChooserButton
from .inputandslider import InputAndSlider
from .spanslider import SpanSlider
from .labeledslider import LabeledSlider
from .waitingspinner import WaitingSpinner
from .markdownwidget import MarkdownWindow
from .imageviewer import ImageViewer
from .popupinfo import PopupInfo
from .selectionwidget import SelectionWidget
from .codeeditor import CodeEditor
from .roundprogressbar import RoundProgressBar

# from .stareditor import StarEditor, StarRating
from .timeline import Timeline, VideoSample

if core.VersionNumber.get_qt_version() < (6, 0, 0):
    from .player import Player

# Deprecated: should be imported from custom_delegates instead
from prettyqt.custom_delegates.buttondelegate import ButtonDelegate
from prettyqt.custom_delegates.radiodelegate import RadioDelegate

__all__ = [
    "Image",
    "ListInput",
    "BoolDictToolButton",
    "OptionalWidget",
    "CollapsibleFrame",
    "ExpandableLine",
    "SingleLineTextEdit",
    "RegexInput",
    "MappedCheckBox",
    "LogTextEdit",
    "FlagSelectionWidget",
    "StringOrNumberWidget",
    "IconLabel",
    "IconWidget",
    "FlowLayout",
    "BorderLayout",
    "SidebarWidget",
    "ColorChooserButton",
    "FileChooserButton",
    "FontChooserButton",
    "InputAndSlider",
    "SpanSlider",
    "LabeledSlider",
    "WaitingSpinner",
    "RoundProgressBar",
    "PopupInfo",
    "ButtonDelegate",
    "RadioDelegate",
    "SelectionWidget",
    "ImageViewer",
    "MarkdownWindow",
    "CodeEditor",
    "Player",
    "Timeline",
    # "StarEditor",
    # "StarRating",
    "VideoSample",
    "RegexEditorWidget",
]
