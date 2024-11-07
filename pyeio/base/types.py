from pathlib import Path
from datetime import datetime, date, time
from typing import Literal, TypeVar, Union

FileExtension = Literal[
    "json",
    "jsonl",
    # "toml",
    # "yaml",
    # "xml",
    # "md",
    # "jpeg",
    # "zst",
    # "nc",
]


VariantFileExtension = Literal[
    "ndjson",
    "jsonlines",
    # "jpg",
    # "yml",
    # "markdown",
]


MimeType = Literal[
    "application/json",
    "application/jsonl",
    # "application/netcdf",
    # "application/x-netcdf",
]

FilePath = str | Path

# ! Python Data Types

JSON_TYPE = TypeVar("JSON_TYPE", bound="JSON")
JSON = Union[
    bool,
    int,
    float,
    str,
    list[JSON_TYPE],
    dict[str, JSON_TYPE],
]

TOML_TYPE = TypeVar("TOML_TYPE", bound="TOML")
TOML = Union[
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
