import sys
from typing import Any, TextIO, Optional, Self, IO

from rich._null_file import NULL_FILE
import rich.file_proxy as rich_file_proxy


class FileProxy(rich_file_proxy.FileProxy):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.debug_file = open(
            "/Users/jevin/code/python/git/enrich/fart4.txt", "w", encoding="utf-8",
        )

    # def write(self, text: str) -> int:
    #     if hasattr(self.__console, "redirect") and self.__console.redirect and self.__console.record:
    #         print("new proxy write special", file=self.debug_file)
    #         # self.__console.record = False
    #         res = super().write(text)
    #         # self.__console.record = True
    #         return res
    #     else:
    #         print("new proxy write normal", file=self.debug_file)
    #         return super().write(text)


    # def flush(self) -> None:
    #     if hasattr(self.__console, "redirect") and self.__console.redirect and self.__console.record:
    #         print("new proxy flush special", file=self.debug_file)
    #         # self.__console.record = False
    #         super().flush()
    #         # self.__console.record = True
    #     else:
    #         print("new proxy flush normal", file=self.debug_file)
    #         return super().flush()

    # @property
    # def rich_proxied_file(self) -> IO[str]:
    #     if hasattr(self.__console, "_in_check_buffer") and self.__console._in_check_buffer:
    #         print("new proxy rich_proxied_file special", file=self.debug_file)
    #         self.debug_file.flush()
    #         return NULL_FILE
    #     else:
    #         print("new proxy rich_proxied_file normal", file=self.debug_file)
    #         self.debug_file.flush()
    #         return super().file

    # def write(self, text: str) -> int:
    #     if hasattr(self.__console, "_in_check_buffer") and self.__console._in_check_buffer:
    #         print("new proxy write special", file=self.debug_file)
    #         self.debug_file.flush()
    #         # return 0
    #         return super().write(text)
    #     else:
    #         print("new proxy write normal", file=self.debug_file)
    #         self.debug_file.flush()
    #         return super().write(text)


    # def flush(self) -> None:
    #     if hasattr(self.__console, "_in_check_buffer") and self.__console._in_check_buffer:
    #         print("new proxy flush special", file=self.debug_file)
    #         self.debug_file.flush()
    #         super().flush()
    #     else:
    #         print("new proxy flush normal", file=self.debug_file)
    #         self.debug_file.flush()
    #         super().flush()