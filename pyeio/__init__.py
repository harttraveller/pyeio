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

from pyeio.io import (
    append,
    read,
    write,
)

if TYPE_CHECKING:
    from pyeio import (
        json,
        jsonl,
        toml,
        yaml,
    )

    # aliases
    from pyeio import jsonl as ndjson
    from pyeio import yaml as yml

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
    "yml",
    "jsonl",
    "ndjson",
]


_dynamic_imports: dict[str, tuple[str, str]] = {
    "json": (__spec__.parent, "__module__"),
    "toml": (__spec__.parent, "__module__"),
    "yaml": (__spec__.parent, "__module__"),
    "jsonl": (__spec__.parent, "__module__"),
}

_aliased_imports: dict[str, str] = {
    "yml": "yaml",
    "ndjson": "jsonl",
}


def __getattr__(name: str) -> object:
    # Resolve aliases first
    canonical = _aliased_imports.get(name, name)

    dynamic_attr = _dynamic_imports.get(canonical)
    if dynamic_attr is None:
        raise AttributeError(name)

    package, module_name = dynamic_attr

    if module_name == "__module__":
        result = import_module(f".{canonical}", package=package)
        globals()[canonical] = result
        # Also cache under the alias if accessed that way
        if name != canonical:
            globals()[name] = result
        return result
    else:
        module = import_module(module_name, package=package)
        result = getattr(module, canonical)
        g = globals()
        for k, (_, v_module_name) in _dynamic_imports.items():
            if v_module_name == module_name:
                g[k] = getattr(module, k)
        # Cache alias
        if name != canonical:
            g[name] = result
        return result


def __dir__() -> list[str]:
    return __all__
