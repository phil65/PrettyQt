"""Module containing custom delegate classes.

PrettyQt offers an extended Item delegate with support for a large number of
different data types.

The following data types are supported:

* bool
* enum.Flag
* enum.Enum
* int
* float
* str
* range
* slice
* list of ints
* list of floats
* list of strings
* pathlib.Path
* re.Pattern
* datetime.date
* datetime.time
* datetime.datetime
* QtCore.QRegularExpression
* QtCore.QTime
* QtCore.QDate
* QtCore.QDateTime
* QtCore.QPoint
* QtCore.QPointF
* QtCore.QRect
* QtCore.QRectF
* QtCore.QRection
* QtCore.QKeyCombination
* QtCore.QLocale
* QtCore.QSize
* QtCore.QSizeF
* QtCore.QUrl
* QtGui.QFont
* QtGui.QKeySequence
* QtGui.QPalette
* QtGui.QColor
* QtGui.QBrush
* QtGui.QCursor
* QtGui.QIcon
* QtWidgets.QSizePolicy

If numpy is installed, the following types are supported, too:

* numpy.floating
* numpy.integer
* numpy.str_
* numpy.datetime64
* numpy.bool_

"""

from .buttondelegate import ButtonDelegate
from .htmlitemdelegate import HtmlItemDelegate, MarkdownItemDelegate
from .icondelegate import IconDelegate
from .nofocusdelegate import NoFocusDelegate
from .progressbardelegate import ProgressBarDelegate
from .radiodelegate import RadioDelegate
from .renderlinkdelegate import RenderLinkDelegate
from .stardelegate import StarDelegate
from .editordelegate import EditorDelegate
from .widgetdelegate import WidgetDelegate


__all__ = [
    "ButtonDelegate",
    "RadioDelegate",
    "ProgressBarDelegate",
    "IconDelegate",
    "StarDelegate",
    "RenderLinkDelegate",
    "NoFocusDelegate",
    "HtmlItemDelegate",
    "MarkdownItemDelegate",
    "WidgetDelegate",
    "EditorDelegate",
]
