from typing import Literal, TypeVar

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


# DataLocation = Literal[
#     "disk",
#     "web",
#     "memory",
# ]
