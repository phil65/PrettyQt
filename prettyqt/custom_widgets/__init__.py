"""Module containing custom widget classes."""

from .image import Image
from .clocklabel import ClockLabel
from .elidedlabel import ElidedLabel
from .listinput import ListInput
from .booldicttoolbutton import BoolDictToolButton
from .optionalwidget import OptionalWidget
from .collapsibleframe import CollapsibleFrame
from .expandableline import ExpandableLine
from .hierarchicalheaderview import HierarchicalHeaderView
from .keycombinationedit import KeyCombinationEdit
from .singlelinetextedit import SingleLineTextEdit
from .rectedit import RectEdit, RegionEdit
from .paletteedit import PaletteEdit
from .cursoredit import CursorEdit
from .iconedit import IconEdit
from .localeedit import LocaleEdit
from .pointedit import PointEdit
from .sizeedit import SizeEdit
from .sizepolicyedit import SizePolicyEdit
from .regexlineedit import RegexLineEdit
from .regexinput import RegexInput
from .mappedcheckbox import MappedCheckBox
from .logtextedit import LogTextEdit
from .flagselectionwidget import FlagSelectionWidget
from .stringornumberwidget import StringOrNumberWidget
from .iconlabel import IconLabel
from .iconbrowser import IconBrowser
from .iconwidget import IconWidget
from .flowlayout import FlowLayout
from .borderlayout import BorderLayout
from .completionwidget import CompletionWidget
from .sidebarwidget import SidebarWidget
from .enumcombobox import EnumComboBox
from .colorcombobox import ColorComboBox
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
from .subsequencecompleter import SubsequenceCompleter
from .framelesswindow import FramelessWindow
from .filetree import FileTree

# from .stareditor import StarEditor, StarRating
from .timeline import Timeline, VideoSample
from .standardiconswidget import StandardIconsWidget


__all__ = [
    "Image",
    "ClockLabel",
    "ElidedLabel",
    "ListInput",
    "BoolDictToolButton",
    "OptionalWidget",
    "CollapsibleFrame",
    "CompletionWidget",
    "ExpandableLine",
    "HierarchicalHeaderView",
    "KeyCombinationEdit",
    "SingleLineTextEdit",
    "RegexLineEdit",
    "RegexInput",
    "MappedCheckBox",
    "LogTextEdit",
    "FlagSelectionWidget",
    "StringOrNumberWidget",
    "IconLabel",
    "IconBrowser",
    "IconWidget",
    "RectEdit",
    "PaletteEdit",
    "CursorEdit",
    "LocaleEdit",
    "IconEdit",
    "PointEdit",
    "SizeEdit",
    "RegionEdit",
    "SizePolicyEdit",
    "FlowLayout",
    "BorderLayout",
    "SidebarWidget",
    "EnumComboBox",
    "ColorComboBox",
    "ColorChooserButton",
    "FileChooserButton",
    "FontChooserButton",
    "InputAndSlider",
    "SpanSlider",
    "LabeledSlider",
    "WaitingSpinner",
    "RoundProgressBar",
    "PopupInfo",
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
    "StandardIconsWidget",
    "SubsequenceCompleter",
    "FramelessWindow",
    "FileTree",
]
