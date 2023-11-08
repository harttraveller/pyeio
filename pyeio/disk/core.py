from pathlib import Path
from typing import Any, Union


class DiskIO:
    def open(self, path: Union[str, Path], auto: bool = True) -> Any:
        pass

    def save(self) -> Any:
        pass


dio = DiskIO()
