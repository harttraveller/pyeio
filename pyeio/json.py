import json
from pathlib import Path
from .core import io


def save(): ...


def load(path: str | Path) -> str | int | float | list | dict:
    return json.loads(io.load_text(path))


# get from web, load into memory
def get(uri: str, shards: int = 1): ...


def put(uri: str, shards: int = 1): ...


# todo
# fix issues with file, like encoding or parsing stuff
# def fix(): ...


# apply operation on file to change
# not too useful here, but useful for recursive apply
# def apply(): ...


# def load_recursive(): ...


# def apply_recursive(): ...

# todo: get recursive from webpage or online directory
# webpage: eg - scrape all json links and download to local dir
# dir: eg - s3 bucket, dl all
