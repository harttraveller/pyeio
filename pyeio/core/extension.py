from typing import Literal, cast

FileExtension = Literal[
    "jsonl",
    "json",
    "toml",
    "xml",
    "md",
    "jpeg",
]

FileExtensionVariant = Literal[
    "ndjson",
    "jsonlines",
    "markdown",
    "jpg",
]

file_extension = FileExtension.__args__

translation: dict[FileExtensionVariant, FileExtension] = {
    "ndjson": "jsonl",
    "jsonlines": "jsonl",
    "jpg": "jpeg",
}


# def standardize(ext: str) -> FileExtension:
#     if ext in translation.keys():
#         return translation[ext]
#     else:
#         return cast(Fil)
