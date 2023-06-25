"""Module containing custom widget classes."""

from .imageviewer import ImageViewer
from .elidedlabel import ElidedLabel
from .editors.listinput import ListInput
from .booldicttoolbutton import BoolDictToolButton
from .optionalwidget import OptionalWidget
from .widgeteditor import WidgetEditor
from .collapsibleframe import CollapsibleFrame
from .clickablelabel import ClickableLabel
from .orientedtableview import OrientedTableView
from .hierarchicalheaderview import HierarchicalHeaderView
from .commandpalette import CommandPalette
from .filterheader import FilterHeader
from .editors.lineedits import IntLineEdit, FloatLineEdit, UrlLineEdit
from .editors.keycombinationedit import KeyCombinationEdit
from .editors.singlelinetextedit import SingleLineTextEdit
from .editors.rectedit import RectEdit, RectFEdit, RegionEdit
from .editors.enumcombobox import EnumComboBox
from .editors.paletteedit import PaletteEdit
from .editors.cursoredit import CursorEdit
from .editors.iconedit import IconEdit
from .editors.localeedit import LocaleEdit
from .editors.pointedit import PointEdit
from .editors.sizeedit import SizeEdit
from .editors.sizepolicyedit import SizePolicyEdit
from .editors.regexlineedit import RegexLineEdit
from .editors.regexinput import RegexInput
from .editors.mappedcheckbox import MappedCheckBox
from .editors.sliceedit import SliceEdit
from .editors.rangeedit import RangeEdit
from .logtextedit import LogTextEdit
from .editors.enumflagwidget import EnumFlagWidget
from .editors.flagselectionwidget import FlagSelectionWidget
from .editors.stringornumberwidget import StringOrNumberWidget
from .iconlabel import IconLabel
from .iconbrowser import IconBrowser
from .iconwidget import IconWidget
from .flowlayout import FlowLayout
from .borderlayout import BorderLayout
from .objectbrowser import ObjectBrowser
from .completionwidget import CompletionWidget
from .sidebarwidget import SidebarWidget
from .editors.colorcombobox import ColorComboBox
from .multicombobox import MultiComboBox
from .editors.colorchooserbutton import ColorChooserButton
from .editors.filechooserbutton import FileChooserButton
from .editors.fontchooserbutton import FontChooserButton
from .editors.inputandslider import InputAndSlider
from .editors.spanslider import SpanSlider, SpanSliderWidget
from .labeledslider import LabeledSlider
from .waitingspinner import WaitingSpinner
from .popupinfo import PopupInfo
from .editors.selectionwidget import SelectionWidget
from .codeeditor import CodeEditor
from .astviewer import AstViewer
from .roundprogressbar import RoundProgressBar
from .subsequencecompleter import SubsequenceCompleter
from .filetree import FileTree
from .scrollareatocwidget import ScrollAreaTocWidget

# from .stareditor import StarEditor, StarRating
from .timeline import Timeline, VideoSample
from .standardiconswidget import StandardIconsWidget


__all__ = [
    "IntLineEdit",
    "FloatLineEdit",
    "UrlLineEdit",
    "ImageViewer",
    "ElidedLabel",
    "ListInput",
    "BoolDictToolButton",
    "OptionalWidget",
    "WidgetEditor",
    "CollapsibleFrame",
    "CompletionWidget",
    "ExpandableLine",
    "CommandPalette",
    "ClickableLabel",
    "OrientedTableView",
    "FilterHeader",
    "HierarchicalHeaderView",
    "KeyCombinationEdit",
    "SingleLineTextEdit",
    "RegexLineEdit",
    "RegexInput",
    "MappedCheckBox",
    "SliceEdit",
    "RangeEdit",
    "LogTextEdit",
    "EnumFlagWidget",
    "FlagSelectionWidget",
    "StringOrNumberWidget",
    "IconLabel",
    "IconBrowser",
    "IconWidget",
    "RectEdit",
    "RectFEdit",
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
    "ObjectBrowser",
    "SidebarWidget",
    "EnumComboBox",
    "ColorComboBox",
    "MultiComboBox",
    "ColorChooserButton",
    "FileChooserButton",
    "FontChooserButton",
    "InputAndSlider",
    "SpanSlider",
    "SpanSliderWidget",
    "LabeledSlider",
    "WaitingSpinner",
    "RoundProgressBar",
    "PopupInfo",
    "SelectionWidget",
    "CodeEditor",
    "Timeline",
    # "StarEditor",
    # "StarRating",
    "AstViewer",
    "VideoSample",
    "StandardIconsWidget",
    "SubsequenceCompleter",
    "FileTree",
    "ScrollAreaTocWidget",
]
