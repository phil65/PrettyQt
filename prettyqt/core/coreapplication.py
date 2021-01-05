from __future__ import annotations

import logging
import os
import pathlib
import sys
from typing import Callable, Dict, List, Optional, Tuple, Union

from prettyqt import constants, core
from prettyqt.qt import QtCore
from prettyqt.utils import InvalidParamError


logger = logging.getLogger(__name__)

QtCore.QCoreApplication.__bases__ = (core.Object,)


class CoreApplication(QtCore.QCoreApplication):
    translators: Dict[str, core.Translator] = dict()

    @classmethod
    def call_on_exit(cls, func: Callable):
        cls.instance().aboutToQuit.connect(func)

    @classmethod
    def get_application_file_path(cls) -> pathlib.Path:
        return pathlib.Path(cls.applicationFilePath())

    @classmethod
    def get_application_dir_path(cls) -> pathlib.Path:
        return pathlib.Path(cls.applicationDirPath())

    @classmethod
    def add_library_path(cls, path: Union[os.PathLike, str]):
        cls.addLibraryPath(os.fspath(path))

    @classmethod
    def get_library_paths(cls) -> List[pathlib.Path]:
        return [pathlib.Path(i) for i in cls.libraryPaths()]

    @classmethod
    def use_hdpi_bitmaps(cls, state: bool = True):
        cls.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, state)

    @classmethod
    def disable_window_help_button(cls, state: bool = True):
        try:
            cls.setAttribute(QtCore.Qt.AA_DisableWindowContextHelpButton, state)
        except AttributeError:
            pass

    def set_metadata(
        self,
        app_name: Optional[str] = None,
        app_version: Union[None, str, QtCore.QVersionNumber, Tuple[int, int, int]] = None,
        org_name: Optional[str] = None,
        org_domain: Optional[str] = None,
    ):
        if app_name is not None:
            self.setApplicationName(app_name)
        if app_version is not None:
            if isinstance(app_version, QtCore.QVersionNumber):
                app_version = app_version.toString()
            elif isinstance(app_version, tuple):
                app_version = ".".join(str(i) for i in app_version)
            self.setApplicationVersion(app_version)
        if org_name is not None:
            self.setOrganizationName(org_name)
        if org_domain is not None:
            self.setOrganizationDomain(org_domain)
        # if sys.platform.startswith("win"):
        #     import ctypes
        #     myappid = 'mycompany.myproduct.subproduct.version' # arbitrary string
        #     ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

    @classmethod
    def load_language_file(cls, file: Union[pathlib.Path, str]) -> core.Translator:
        translator = core.Translator()
        translator.load_file(file)
        cls.installTranslator(translator)
        cls.translators[str(file)] = translator
        return translator

    @classmethod
    def load_language(cls, language: str) -> core.Translator:
        translator = core.Translator.for_language(language)
        cls.installTranslator(translator)
        cls.translators[language] = translator
        return translator

    def post_event(
        self,
        obj: QtCore.QObject,
        event: QtCore.QEvent,
        priority: Union[int, constants.EventPriorityStr] = "normal",
    ):
        if isinstance(priority, int):
            prio = priority
        else:
            if priority not in constants.EVENT_PRIORITY:
                raise InvalidParamError(priority, constants.EVENT_PRIORITY)
            prio = constants.EVENT_PRIORITY[priority]
        return self.postEvent(obj, event, prio)

    def main_loop(self) -> int:
        return self.exec_()

    @staticmethod
    def restart():
        os.execl(sys.executable, sys.executable, *sys.argv)
