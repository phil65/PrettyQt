# -*- coding: utf-8 -*-

"""custom_widgets module

"""

from .image import Image
from .listinput import ListInput
from .booldicttoolbutton import BoolDictToolButton
from .optionalwidget import OptionalWidget
from .singlelinetextedit import SingleLineTextEdit
from .mappedcheckbox import MappedCheckBox
from .promptlineedit import PromptLineEdit
from .stringornumberwidget import StringOrNumberWidget
from .iconlabel import IconLabel
from .flowlayout import FlowLayout
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
from .buttondelegate import ButtonDelegate
from .radiodelegate import RadioDelegate
from .selectionwidget import SelectionWidget
from .codeeditor import CodeEditor
from .regexeditor.editor import RegexEditorWidget

__all__ = ["Image",
           "ListInput",
           "BoolDictToolButton",
           "OptionalWidget",
           "SingleLineTextEdit",
           "MappedCheckBox",
           "PromptLineEdit",
           "StringOrNumberWidget",
           "IconLabel",
           "FlowLayout",
           "ColorChooserButton",
           "FileChooserButton",
           "FontChooserButton",
           "InputAndSlider",
           "SpanSlider",
           "LabeledSlider",
           "WaitingSpinner",
           "PopupInfo",
           "ButtonDelegate",
           "RadioDelegate",
           "SelectionWidget",
           "ImageViewer",
           "MarkdownWindow",
           "CodeEditor",
           "RegexEditorWidget"]
