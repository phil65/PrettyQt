# -*- coding: utf-8 -*-

from qtpy import QtWidgets


STYLES = dict(
    close=QtWidgets.QStyle.SP_TitleBarCloseButton,
    maximise=QtWidgets.QStyle.SP_TitleBarMaxButton,
    information=QtWidgets.QStyle.SP_MessageBoxInformation,
    warning=QtWidgets.QStyle.SP_MessageBoxWarning,
    critical=QtWidgets.QStyle.SP_MessageBoxCritical,
    question=QtWidgets.QStyle.SP_MessageBoxQuestion,
)


class Style(QtWidgets.QStyle):
    pass
