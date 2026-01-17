# ruff: noqa
from json import (
    dump,
    dumps,
    load,
    loads,
    detect_encoding,
)
from orjson import (
    JSONDecodeError,
    JSONEncodeError,
)

from ._json import (
    read,
    write,
    serialize,
    parse,
)
