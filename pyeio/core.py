"""
Primary interface class

TODO (maybe)
- add callable to convert or transform data types and formats in easy call
    - add **kwargs to customize the transformation (ie: for loading dataframe with list orientation)
"""

from pathlib import Path
from typing import Any
from pyeio.utils import file_format, data_type
from pyeio.form import JSON, JSONL


class EIO:
    def __init__(self):
        self.__init_interfaces()
        self.__init_methods()

    def __init_interfaces(self) -> None:
        self.json = JSON()
        self.jsonl = JSONL()

    def __init_methods(self) -> None:
        self.__methods = {
            "json": {"save": self.json.save, "load": self.json.load},
            "jsonl": {"save": self.jsonl.save, "load": self.jsonl.load},
        }

    @property
    def formats(self) -> set[str]:
        return set(self.__methods.keys())

    def __check_supported(self, fmt: str) -> None:
        if fmt not in self.formats:
            raise ValueError("Unsupported file format.")

    def load(self, path: str | Path) -> Any:
        """
        Load a file into memory.

        Args:
            path (str | Path): Path to file.

        Returns:
            Any: Loaded data object.
        """
        fmt = file_format(path)
        self.__check_supported(fmt)
        data = self.__methods[fmt]["load"](path)
        return data

    def save(self, data: Any, path: str | Path) -> None:
        """
        Save a file in memory to disk.

        Args:
            data (Any): Data object to save.
            path (str | Path): Path to save data at.
        """
        fmt = file_format(path)
        self.__check_supported(fmt)
        self.__methods[fmt]["save"](data, path)
