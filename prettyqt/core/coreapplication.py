from __future__ import annotations

from collections.abc import Callable
import logging
import os
import pathlib
import sys

from prettyqt import constants, core
from prettyqt.utils import datatypes


logger = logging.getLogger(__name__)


class CoreApplicationMixin(core.ObjectMixin):
    translators: dict[str, core.Translator] = {}

    @classmethod
    def call_on_exit(cls, func: Callable):
        instance = cls.instance()
        if instance is None:
            raise RuntimeError("No QApplication running")
        instance.aboutToQuit.connect(func)

    @classmethod
    def get_application_file_path(cls) -> pathlib.Path:
        return pathlib.Path(cls.applicationFilePath())

    @classmethod
    def get_application_dir_path(cls) -> pathlib.Path:
        return pathlib.Path(cls.applicationDirPath())

    @classmethod
    def add_library_path(cls, path: datatypes.PathType):
        cls.addLibraryPath(os.fspath(path))

    @classmethod
    def get_library_paths(cls) -> list[pathlib.Path]:
        return [pathlib.Path(i) for i in cls.libraryPaths()]

    def set_application_name(self, name: str):
        if os.name == "nt" and name and not getattr(sys, "frozen", False):
            import ctypes

            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(name)
        self.setApplicationName(name)

    def set_metadata(
        self,
        app_name: str | None = None,
        app_version: None | datatypes.SemanticVersionType = None,
        org_name: str | None = None,
        org_domain: str | None = None,
    ):
        if app_name is not None:
            self.setApplicationName(app_name)
        match app_version:
            case None:
                pass
            case core.QVersionNumber():
                app_version = app_version.toString()
                self.setApplicationVersion(app_version)
            case tuple():
                app_version = ".".join(str(i) for i in app_version)
                self.setApplicationVersion(app_version)
            case str():
                self.setApplicationVersion(app_version)
            case _:
                raise TypeError(app_version)
        if org_name is not None:
            self.setOrganizationName(org_name)
        if org_domain is not None:
            self.setOrganizationDomain(org_domain)

    @classmethod
    def load_language_file(cls, file: datatypes.PathType) -> core.Translator:
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
        obj: core.QObject,
        event: core.QEvent,
        priority: int | constants.EventPriorityStr = "normal",
    ):
        match priority:
            case int():
                prio = priority
            case str():
                prio = constants.EVENT_PRIORITY[priority]
            case _:
                raise TypeError(priority)
        return self.postEvent(obj, event, prio)

    def in_main_thread(self) -> bool:
        """Check if we are in the thread in which QApplication object was created.

        Returns:
            True if we are in the main thread, False otherwise.
        """
        return self.thread() == core.Thread.currentThread()

    def main_loop(self) -> int:
        return self.exec()

    @staticmethod
    def restart():
        os.execl(sys.executable, sys.executable, *sys.argv)
        # process = QProcess()
        # process.setProgram(sys.executable)

        # if not running_as_bundled_app():
        #     process.setArguments(sys.argv)

        # process.startDetached()
        # self.close(quit_app=True)


class CoreApplication(CoreApplicationMixin, core.QCoreApplication):
    pass
