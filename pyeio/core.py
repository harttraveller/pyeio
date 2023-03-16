"""
Primary interface class

TODO (maybe)
- add callable to convert or transform data types and formats in easy call
    - add **kwargs to customize the transformation (ie: for loading dataframe with list orientation)
"""

from pathlib import Path
from typing import Any, Callable
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
        Description

        Args:
            path (str | Path): _description_
            form (str, optional): _description_. Defaults to "auto".

        Returns:
            Any: _description_
        """
        file_format = self.io.query.file_format(path)
        assert file_format in self.io.formats, "unsupported file format"
        data = self.__methods[file_format]["load"](path)
        return data

    def save(self, data: Any, path: str | Path) -> None:
        """
        Description

        Args:
            data (Any): _description_
            path (str | Path): _description_

        Notes:
            - Auto detects save type based on file extension.
        """
        target = self.io.query.file_format(path)
        assert target in self.io.formats, "unsupported file format"
        kind = self.io.query.data_type(data)
        assert self.io.transform.valid(target, kind), "invalid target format"
        data = self.io.transform.__methods[target][kind](data)
        self.io._id[target]["save"](data, path)
