from pathlib import Path


class Query:
    @staticmethod
    def file_name(path: str | Path) -> str:
        "get file name from path"
        return str(path).split("/")[-1]

    @staticmethod
    def file_format(path: str | Path) -> str:
        "get file format from path"
        return Query.file_name(path).split(".")[-1]

    @staticmethod
    def file_size(path: str | Path) -> int:
        "get file size in bytes from path"
        raise NotImplementedError()

    @staticmethod
    def data_type(obj: Any) -> str:
        "get object type as string"
        return str(type(obj)).split("'")[-2]

    @staticmethod
    def read():
        pass
