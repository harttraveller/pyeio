import json
from pathlib import Path
from .core import io


def save(): ...


def load(path: str | Path) -> list | dict:
    return json.loads(io.load_text(path))


# todo
# fix issues with file, like encoding or parsing stuff
# def fix(): ...


# apply operation on file to change
# not too useful here, but useful for recursive apply
# def apply(): ...


# def load_recursive(): ...


# def apply_recursive(): ...
