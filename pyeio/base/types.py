from pathlib import Path
from datetime import datetime, date, time
from typing import Literal, TypeVar, Union

FileFormatModule = Literal[
    "json",
    "jsonl",
    "toml",
    "yaml",
]

StandardFileExtension = FileFormatModule


VariantFileExtension = Literal[
    "ndjson",
    "jsonlines",
    "yml",
]

FileExtension = StandardFileExtension | VariantFileExtension

MimeType = Literal[
    "application/json",
    "application/jsonl",
]

FilePath = str | Path

# ! Python Data Types

JSON_TYPE = TypeVar("JSON_TYPE", bound="PyJSON")
PyJSON = Union[
    bool,
    int,
    float,
    str,
    list[JSON_TYPE],
    dict[str, JSON_TYPE],
]
SerializedJSON = str | bytes | bytearray

TOML_TYPE = TypeVar("TOML_TYPE", bound="PyTOML")
PyTOML = Union[
    bool,
    int,
    float,
    str,
    datetime,
    date,
    time,
    list[TOML_TYPE],
    dict[str, TOML_TYPE],
]

# ! ---

# DataLocation = Literal[
#     "disk",
#     "web",
#     "memory",
# ]
