import json
from pathlib import Path
from .core import io


def save(): ...


def load(path: str | Path) -> str | int | list | dict:
    return json.loads(io.load_text(path))


# fetch from web
def fetch(): ...


def download(): ...


# todo
# fix issues with file, like encoding or parsing stuff
# def fix(): ...


# apply operation on file to change
# not too useful here, but useful for recursive apply
# def apply(): ...


# def load_recursive(): ...


# def apply_recursive(): ...
