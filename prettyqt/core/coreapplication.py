import logging
import os
import pathlib
import sys
from typing import Callable, List, Optional, Set, Union

from prettyqt import constants, core
from prettyqt.qt import QtCore
from prettyqt.utils import InvalidParamError


logger = logging.getLogger(__name__)

QtCore.QCoreApplication.__bases__ = (core.Object,)


LOCALIZATION_PATH = pathlib.Path(__file__).parent.parent / "localization"


class CoreApplication(QtCore.QCoreApplication):
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
    def add_library_path(cls, path: Union[pathlib.Path, str]):
        cls.addLibraryPath(str(path))

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
        app_version: Optional[str] = None,
        org_name: Optional[str] = None,
        org_domain: Optional[str] = None,
    ):
        if app_name is not None:
            self.setApplicationName(app_name)
        if app_version is not None:
            self.setApplicationVersion(app_name)  # type: ignore
        if org_name is not None:
            self.setOrganizationName(org_name)
        if org_domain is not None:
            self.setOrganizationDomain(org_domain)
        # import ctypes
        # myappid = 'mycompany.myproduct.subproduct.version' # arbitrary string
        # ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

    def load_language_file(self, file: Union[pathlib.Path, str]) -> core.Translator:
        translator = core.Translator(self)
        if file in ["de", "fr"]:
            file = LOCALIZATION_PATH / f"qtbase_{file}.ts"
        translator.load_file(file)
        self.installTranslator(translator)
        return translator

    def get_available_languages(self) -> Set[str]:
        return {
            str(path).split("_", maxsplit=1)[1][:-3]
            for path in LOCALIZATION_PATH.iterdir()
        }

    def load_language(self, language: str):
        translator = core.Translator(self)
        if language not in self.get_available_languages():
            raise ValueError("Language does not exist")
        for file in LOCALIZATION_PATH.iterdir():
            if file.stem.endswith(f"_{language}"):
                path = LOCALIZATION_PATH / file.name
                translator.load_file(path)
                logger.debug(f"loading {path}")
                self.installTranslator(translator)

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
