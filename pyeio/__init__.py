from pathlib import Path
from typing import Any
from pyeio.core import utils

# todo.fix: figure out how to do proper type hints
# todo: need to add format identification and dynamic module loading based on format to avoid taking a massive amount of time to import


def open(path: str | Path) -> Any: ...


def save(): ...


def load(): ...


def download(): ...
