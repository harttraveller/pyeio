"""
Primary interface class

TODO (maybe)
- add callable to convert or transform data types and formats in easy call
    - add **kwargs to customize the transformation (ie: for loading dataframe with list orientation)
"""

from pathlib import Path
from typing import Any
from pyeio.utils import file_format
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

    def _check_supported(self, fmt: str) -> None:
        if fmt not in self.formats:
            raise ValueError("Unsupported file format.")

    def load(self, path: str | Path, custom: str | None = None) -> Any:
        """
        Load a file into memory.

        Args:
            path (str | Path): Path to file.
            custom (str | None): Load a non extension aligned file. Defaults to None.

        Returns:
            Any: Loaded data object.
        """
        fmt = file_format(path)
        self._check_supported(fmt)
        if custom is None:
            data = self.__methods[fmt]["load"](path)
        else:
            self._check_supported(custom)
            data = self.__methods[custom]["load"](path)
        return data

    def save(self, data: Any, path: str | Path, custom: str | None = None) -> None:
        """
        Save a file in memory to disk.

        Args:
            data (Any): Data object to save.
            path (str | Path): Path to save data at.
            custom (str | None): Save a non extension aligned file. Defaults to None.
        """
        fmt = file_format(path)
        self._check_supported(fmt)
        if custom is None:
            self.__methods[fmt]["save"](data, path)
        else:
            self._check_supported(custom)
            self.__methods[custom]["save"](data, path)

    def add(self, data: Any, path: str | Path, custom: str | None = None) -> None:
        # TODO: method for adding data, eg: writing at end of jsonl or adding to sqlite db
        pass


"""
TODO:
- implement pipeline class that allows loading and format transformations with load
    - useful when you want to load a zip file with internal formats, for instance
"""


class Pipeline:
    pass


"""
TODO:
- implement generator that can load in extremely large files piece by piece and handle each piece of component data by passing it to a handler agent
"""


class Generator:
    pass
