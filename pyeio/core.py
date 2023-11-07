"""
Primary interface class

TODO (maybe)
- add callable to convert or transform data types and formats in easy call
    - add **kwargs to customize the transformation (ie: for loading dataframe with list orientation)
"""

from pathlib import Path
from typing import Any, Union, Optional
from pyeio.util import file_format
from pyeio.schema import JSON, JSONL


class IO:
    def open():
        # should return inferred data type
        pass

    def save():
        # should save inferred data type
        pass

    def load():
        # should return format representation object
        pass

    def make():
        # should return format representation object, creating disk object (ie: for databases)
        pass


# from pathlib import Path
# from typing import Optional, Union
# from pydantic import BaseModel, field_validator


# class DataFormat(BaseModel):
#     extension: str

#     # @field_validator("extension")
#     # def __validate_name(cls, extension: str) -> str:
#     #     if (extension not in extset) or (extension != "unknown"):
#     #         # ? redundant
#     #         raise ValueError("unknown file format")
#     #     return extension

#     def __str__(self) -> str:
#         return self.extension

#     def __repr__(self) -> str:
#         return self.extension


# class ResolutionResult(BaseModel):
#     success: bool
#     dformat: DataFormat


# class Resolver:
#     def __init__(self):
#         pass


# def resolve_via_loc(loc: Union[str, Path], val: bool) -> ResolutionResult:
#     loc = str(loc)
#     if "." in loc:
#         extension = loc.split(".")[-1].lower()
#         if extension in extset:
#             return ResolutionResult(success=True, dformat=DataFormat(extension=extension))
#         else:
#             return ResolutionResult(
#                 success=False, dformat=DataFormat(extension="unknown")
#             )
#     else:
#         # todo: if val, load
#         # todo: if url/uri, doublecheck by retrieving from web
#         # todo: if path, doublecheck by loading in
#         raise NotImplementedError(
#             "Could not resolve from file extension, would need to read in file "
#             "to resolve from binary, but this feature is currently unimplemented."
#         )


# def resolve_via_raw(raw: Union[str, bytes]) -> ResolutionResult:
#     pass


# def resolve(
#     raw: Optional[Union[str, bytes]] = None,
#     loc: Optional[Union[str, Path]] = None,
#     val: bool = False,
# ) -> DataFormat:
#     """
#     raw: text
#     loc: path (str/Path) or uri/url to resource
#     """
#     if val:
#         raise NotImplementedError(
#             "Reading in the resource to check it is not yet supported, "
#             "you should read it in and pass the text or binary data to this function."
#         )
#     # check if appropriate params have been passed in
#     if all([raw is None, loc is None]):
#         raise ValueError("You must pass an argument to at least one of the parameters.")
#     # assess if the path or uri
#     # todo: if val, run all, compare results
#     if loc is not None:
#         loc_resolution_attempt = resolve_via_loc(loc=loc, val=val)
#         if loc_resolution_attempt.success:
#             # todo: if val, doublecheck by reading in
#             return loc_resolution_attempt.dformat
#     if raw is not None:
#         raw_resolution_attempt = resolve_via_raw(raw=raw)
#         if raw_resolution_attempt.success:
#             return raw_resolution_attempt.dformat
#     # todo: check to make sure there are no dataformats called 'unknown'
#     return "unknown"


# class EIO:
#     def __init__(self):
#         self.__init_interfaces()
#         self.__init_methods()

#     def __init_interfaces(self) -> None:
#         self.json = JSON()
#         self.jsonl = JSONL()

#     def __init_methods(self) -> None:
#         self.__methods = {
#             "json": {"save": self.json.save, "load": self.json.load},
#             "jsonl": {"save": self.jsonl.save, "load": self.jsonl.load},
#         }

#     @property
#     def formats(self) -> set[str]:
#         return set(self.__methods.keys())

#     def _check_supported(self, fmt: str) -> None:
#         if fmt not in self.formats:
#             raise ValueError("Unsupported file format.")

#     def load(self, path: Union[str, Path], custom: Optional[str] = None) -> Any:
#         """
#         Load a file into memory.

#         Args:
#             path (str | Path): Path to file.
#             custom (str | None): Load a non extension aligned file. Defaults to None.

#         Returns:
#             Any: Loaded data object.
#         """
#         fmt = file_format(path)
#         self._check_supported(fmt)
#         if custom is None:
#             data = self.__methods[fmt]["load"](path)
#         else:
#             self._check_supported(custom)
#             data = self.__methods[custom]["load"](path)
#         return data

#     def save(
#         self,
#         data: Any,
#         path: Union[str, Path],
#         custom: Optional[str] = None,
#     ) -> None:
#         """
#         Save a file in memory to disk.

#         Args:
#             data (Any): Data object to save.
#             path (str | Path): Path to save data at.
#             custom (str | None): Save a non extension aligned file. Defaults to None.
#         """
#         fmt = file_format(path)
#         self._check_supported(fmt)
#         if custom is None:
#             self.__methods[fmt]["save"](data, path)
#         else:
#             self._check_supported(custom)
#             self.__methods[custom]["save"](data, path)

#     def add(
#         self,
#         data: Any,
#         path: Union[str, Path],
#         custom: Optional[str] = None,
#     ) -> None:
#         # TODO: method for adding data, eg: writing at end of jsonl or adding to sqlite db
#         pass


# """
# TODO:
# - implement pipeline class that allows loading and format transformations with load
#     - useful when you want to load a zip file with internal formats, for instance
# """


# class Pipeline:
#     pass


# """
# TODO:
# - implement generator that can load in extremely large files piece by piece and handle each piece of component data by passing it to a handler agent
# """


# class Generator:
#     pass
