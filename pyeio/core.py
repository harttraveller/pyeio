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

    def load(self, path: str | Path) -> Any:
        """
        Load a file into memory.

        Args:
            path (str | Path): Path to file.

        Returns:
            Any: Loaded data object.
        """
        fmt = file_format(path)
        if fmt not in self.formats:
            raise ValueError("Unsupported file format.")
        data = self.__methods[fmt]["load"](path)
        return data

    def save(self, data: Any, path: str | Path) -> None:
        """
        Save a file in memory to disk.

        Args:
            data (Any): Data object to save.
            path (str | Path): Path to save data at.
        """
        target = file_format(path)
        assert target in self.io.formats, "unsupported file format"
        kind = self.io.query.data_type(data)
        assert self.io.transform.valid(target, kind), "invalid target format"
        data = self.io.transform.__methods[target][kind](data)
        self.io._id[target]["save"](data, path)
