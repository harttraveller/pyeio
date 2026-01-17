from builtins import open
from importlib import import_module
from io import (
    DEFAULT_BUFFER_SIZE,
    SEEK_CUR,
    SEEK_END,
    SEEK_SET,
    BlockingIOError,
    BufferedIOBase,
    BufferedRandom,
    BufferedReader,
    BufferedRWPair,
    BufferedWriter,
    BytesIO,
    FileIO,
    IncrementalNewlineDecoder,
    IOBase,
    RawIOBase,
    StringIO,
    TextIOBase,
    TextIOWrapper,
    UnsupportedOperation,
    open_code,
    text_encoding,
)
from typing import TYPE_CHECKING

# io extras
from pyeio.io import (
    append,
    read,
    write,
)

if TYPE_CHECKING:
    from pyeio import json, toml, yaml

__all__ = [
    # passthrough
    "open",
    "DEFAULT_BUFFER_SIZE",
    "SEEK_CUR",
    "SEEK_END",
    "SEEK_SET",
    "BlockingIOError",
    "BufferedIOBase",
    "BufferedRandom",
    "BufferedReader",
    "BufferedRWPair",
    "BufferedWriter",
    "BytesIO",
    "FileIO",
    "IncrementalNewlineDecoder",
    "IOBase",
    "RawIOBase",
    "StringIO",
    "TextIOBase",
    "TextIOWrapper",
    "UnsupportedOperation",
    "open_code",
    "text_encoding",
    # custom
    "read",
    "write",
    "append",
    # formats
    "json",
    "toml",
    "yaml",
]


_dynamic_imports: dict[str, tuple[str, str]] = {
    "json": (__spec__.parent, "__module__"),
    "toml": (__spec__.parent, "__module__"),
    "yaml": (__spec__.parent, "__module__"),
}


def __getattr__(attr_name: str) -> object:
    if attr_name in _deprecated_dynamic_imports:
        from pydantic.warnings import PydanticDeprecatedSince20

        warn(
            f"Importing {attr_name} from `pydantic` is deprecated. This feature is either no longer supported, or is not public.",
            PydanticDeprecatedSince20,
            stacklevel=2,
        )

    dynamic_attr = _dynamic_imports.get(attr_name)
    if dynamic_attr is None:
        return _getattr_migration(attr_name)

    package, module_name = dynamic_attr

    if module_name == "__module__":
        result = import_module(f".{attr_name}", package=package)
        globals()[attr_name] = result
        return result
    else:
        module = import_module(module_name, package=package)
        result = getattr(module, attr_name)
        g = globals()
        for k, (_, v_module_name) in _dynamic_imports.items():
            if v_module_name == module_name and k not in _deprecated_dynamic_imports:
                g[k] = getattr(module, k)
        return result
