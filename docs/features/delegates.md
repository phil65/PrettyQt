Delegates
======

Several additional delegates are supplied by PrettyQt.
- HtmlItemDelegate (supports HTML for text)
- IconDelegate
- NoFocusDelegate (hides focus frame)
- ProgressBarDelegate (displays a percentage value as a progress bar)
- RadioDelegate
- RenderLinkDelegate (renders a string as link and makes it clickable)
- StarDelegate ()
- VariantDelegate (regular delegate supporting many data types)
- WidgetDelegate (experimental)

The main one is "VariantDelegate", which basically works
like the default delegate, but supports editing a larger amount
of datatypes.

The following data types are supported:

- bool
- enum.Flag
- enum.Enum
- int
- float
- str
- range
- slice
- list of ints
- list of floats
- list of strings
- pathlib.Path
- re.Pattern
- datetime.date
- datetime.time
- datetime.datetime
- QtCore.QRegularExpression
- QtCore.QTime
- QtCore.QDate
- QtCore.QDateTime
- QtCore.QPoint
- QtCore.QPointF
- QtCore.QRect
- QtCore.QRectF
- QtCore.QRection
- QtCore.QKeyCombination
- QtCore.QLocale
- QtCore.QSize
- QtCore.QSizeF
- QtCore.QUrl
- QtGui.QFont
- QtGui.QKeySequence
- QtGui.QPalette
- QtGui.QColor
- QtGui.QCursor
- QtGui.QIcon
- QtWidgets.QSizePolicy

If numpy is installed, the following types are supported, too:

- numpy.floating
- numpy.integer
- numpy.str_
- numpy.datetime64
- numpy.bool_
