"""Module that helps integrating with rich library."""
import os
import sys
from typing import Any, TextIO, Optional, Self, IO

import rich.console as rich_console
from rich import inspect as rinspect
from rich import print as rprint
from rich.ansi import AnsiDecoder
# from rich.file_proxy import FileProxy
from .file_proxy import FileProxy
from rich._null_file import NULL_FILE


class OriginalStdioSingleton:
    _instance: Optional[Self] = None
    _stdout: Optional[TextIO] = None
    _stderr: Optional[TextIO] = None
    
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._stdout = sys.stdout
            cls._stderr = sys.stderr
            cls._instance = super(OriginalStdioSingleton, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    @property
    def stdout(self):
        return self._stdout

    @property
    def stderr(self):
        return self._stderr


OriginalStdioSingleton()


class Console(rich_console.Console):
    """Extends rich Console class."""

    def __init__(self, *args: str, redirect: bool = True, **kwargs: Any) -> None:
        """
        enrich console does soft-wrapping by default and this diverge from
        original rich console which does not, creating hard-wraps instead.
        """
        self.redirect = redirect

        if "soft_wrap" not in kwargs:
            kwargs["soft_wrap"] = True

        # Unless user already mentioning terminal preference, we use our
        # heuristic to make an informed decision.
        if "force_terminal" not in kwargs:
            kwargs["force_terminal"] = should_do_markup(
                stream=kwargs.get("file", sys.stdout)
            )

        super().__init__(*args, **kwargs)
        self.extended = True
        self.debug_file = open(
            "/Users/jevin/code/python/git/enrich/fart2.txt", "w", encoding="utf-8",
        )
        # rprint(self, file=self.debug_file)
        # rprint("\n\n!!!\n\n", file=self.debug_file)
        # if self._file:
        #     f3 = self._file
        #     rprint("using self._file", file=self.debug_file)
        # elif self.stderr:
        #     f3 = sys.stderr
        #     rprint("using sys.stderr", file=self.debug_file)
        # else:
        #     f3 = sys.stdout
        #     rprint("using sys.stdout", file=self.debug_file)
        # rprint(
        #     f"f3 getattr rich_proxied_file: {getattr(f3, 'rich_proxied_file', 'foobar')}",
        #     file=self.debug_file,
        # )
        # rprint("\n\n!!!\n\n", file=self.debug_file)
        # rc = rich_console.Console(file=self.debug_file)
        # rinspect(self.file, console=rc, all=True)
        # rprint("\n\n!!!\n\n", file=self.debug_file)
        # rinspect(self, console=rc, all=True)

        self._orig_stdout = None
        self._orig_stderr = None
        self._in_check_buffer = False

        print(f"new pre _file: {self._file} file id: {id(self.file)} stdout id: {id(sys.stdout)} stderr id: {id(sys.stderr)}", file=self.debug_file)
        self.debug_file.flush()

        if self.redirect:
            if not hasattr(sys.stdout, "rich_proxied_file"):
                self._orig_stdout = OriginalStdioSingleton().stdout
                sys.stdout = FileProxy(self, self._orig_stdout)  # type: ignore
            if not hasattr(sys.stderr, "rich_proxied_file"):
                self._orig_stderr = OriginalStdioSingleton().stderr
                sys.stderr = FileProxy(self, self._orig_stderr)  # type: ignore

        print(f"new post _file: {self._file} file id: {id(self.file)} stdout id: {id(sys.stdout)} stderr id: {id(sys.stderr)} orig_stdout id: {id(self._orig_stdout)} orig_stderr id: {id(self._orig_stderr)}", file=self.debug_file)

        # print(sys.stdout.rich_proxied_file)
        # assert hasattr(sys.stdout, "rich_proxied_file")

    # def _check_buffer(self) -> None:
    #     print(f"new _check_buffer redirect: {self.redirect} record: {self.record} _file: {self._file} file id: {id(self.file)} stdout id: {id(sys.stdout)} stderr id: {id(sys.stderr)} orig_stdout id: {id(self._orig_stdout)} orig_stderr id: {id(self._orig_stderr)}", file=self.debug_file)
    #     self.debug_file.flush()
    #     # if self.redirect and self.record:
    #     #     file = self.file
    #     #     if (hasattr(self, "_orig_stdout") and file is self._orig_stdout) or (hasattr(self, "_orig_stderr") and hasattr(self, "orig_stderr") and file is self._orig_stderr):
    #     #         # assert False and "bailing out"
    #     #         return
    #     if self.redirect and self.record:
    #         file = self.file
    #         if (hasattr(self, "_orig_stdout") and file is self._orig_stdout) or (hasattr(self, "_orig_stderr") and hasattr(self, "orig_stderr") and file is self._orig_stderr):
    #             # assert False and "bailing out"
    #             return
    #     super()._check_buffer()

    # def _check_buffer(self) -> None:
    #     if self.redirect and self.record:
    #         # self.record = False
    #         super()._check_buffer()
    #         # self.record = True
    #     else:
    #         super._check_buffer()

    def _check_buffer(self) -> None:
        self._in_check_buffer = True
        super()._check_buffer()
        self._in_check_buffer = False
        # if self.redirect and self.record:
        #     # self.record = False
        #     super()._check_buffer()
        #     # self.record = True
        # else:
        #     super._check_buffer()

    @property
    def file(self) -> IO[str]:
        f = super().file
        if self.redirect and hasattr(self, "_in_check_buffer") and self._in_check_buffer:
            print(f"new _file special", file=self.debug_file)
            self.debug_file.flush()
            return NULL_FILE
        else:
            print(f"new _file normal", file=self.debug_file)
            self.debug_file.flush()
            return f


    # @property
    # def record(self) -> bool:
    #     file = self.file
    #     print(f"new record file id {id(file)}", file=self.debug_file)
    #     if file in (self._orig_stdout, self._orig_stderr):
    #         print("new record returning False", file=self.debug_file)
    #         return False
    #     return super().record

    # https://github.com/python/mypy/issues/4441
    def print(self, *args, **kwargs) -> None:  # type: ignore
        """Print override that respects user soft_wrap preference."""
        # Currently rich is unable to render ANSI escapes with print so if
        # we detect their presence, we decode them.
        # https://github.com/willmcgugan/rich/discussions/404
        if args and isinstance(args[0], str) and "\033" in args[0]:
            text = format(*args) + "\n"
            decoder = AnsiDecoder()
            args = list(decoder.decode(text))  # type: ignore
        super().print(*args, **kwargs)


# Based on Ansible implementation
def to_bool(value: Any) -> bool:
    """Return a bool for the arg."""
    if value is None or isinstance(value, bool):
        return bool(value)
    if isinstance(value, str):
        value = value.lower()
    if value in ("yes", "on", "1", "true", 1):
        return True
    return False


def should_do_markup(stream: TextIO = sys.stdout) -> bool:
    """Decide about use of ANSI colors."""
    py_colors = None

    # https://xkcd.com/927/
    for env_var in ["PY_COLORS", "CLICOLOR", "FORCE_COLOR", "ANSIBLE_FORCE_COLOR"]:
        value = os.environ.get(env_var, None)
        if value is not None:
            py_colors = to_bool(value)
            break

    # If deliverately disabled colors
    if os.environ.get("NO_COLOR", None):
        return False

    # User configuration requested colors
    if py_colors is not None:
        return to_bool(py_colors)

    term = os.environ.get("TERM", "")
    if "xterm" in term:
        return True

    if term == "dumb":
        return False

    # Use tty detection logic as last resort because there are numerous
    # factors that can make isatty return a misleading value, including:
    # - stdin.isatty() is the only one returning true, even on a real terminal
    # - stderr returting false if user user uses a error stream coloring solution
    return stream.isatty()
