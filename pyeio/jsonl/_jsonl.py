from __future__ import annotations

from pathlib import Path
from typing import (
    Any,
    AnyStr,
    Callable,
    Iterable,
    Iterator,
    cast,
    overload,
)

import orjson

from pyeio import io
from pyeio.annotations import (
    JsonSerializable,
    T_PydanticModel,
)
from pyeio.json import serialize as json_serialize

__all__ = [
    "iter_parse",
    "iter_read",
    "parse",
    "read",
    "serialize",
    "write",
    "append",
    "extend",
]


def _iter_lines(data: str | bytes) -> Iterator[bytes]:
    """Yields non-empty lines from raw JSONL data as bytes."""
    if isinstance(data, str):
        data = data.encode("utf-8")
    elif not isinstance(data, bytes):
        raise TypeError(data)
    for line in data.split(b"\n"):
        line = line.strip()
        if line:
            yield line


def _serialize_one(
    obj: JsonSerializable,
    fallback: Callable[[Any], Any] | None = None,
) -> bytes:
    """Serializes a single object to a JSON bytes line (no trailing newline)."""
    if hasattr(obj, "__pydantic_core_schema__"):
        return json_serialize(obj, returns=bytes, fallback=fallback)  # type: ignore[arg-type]
    else:
        return orjson.dumps(
            obj,
            default=fallback,
            option=orjson.OPT_NON_STR_KEYS | orjson.OPT_OMIT_MICROSECONDS,
        )


@overload
def iter_parse(
    data: str | bytes,
    /,
    *,
    n: int | None = None,
) -> Iterator[Any]: ...
@overload
def iter_parse(
    data: str | bytes,
    model: type[T_PydanticModel],
    /,
    strict: bool | None = None,
    context: Any | None = None,
    by_alias: bool | None = None,
    by_name: bool | None = None,
    *,
    n: int | None = None,
) -> Iterator[T_PydanticModel]: ...
def iter_parse(
    data: str | bytes,
    model: type[T_PydanticModel] | None = None,
    /,
    strict: bool | None = None,
    context: Any | None = None,
    by_alias: bool | None = None,
    by_name: bool | None = None,
    *,
    n: int | None = None,
) -> Iterator[Any] | Iterator[T_PydanticModel]:
    """
    Lazily parses JSONL data, yielding one object per line.

    When no model is provided, each line is parsed into standard Python types.
    When a model is provided, each line is validated against the Pydantic model.

    Args:
        data (str | bytes): JSONL data as string or bytes to be parsed.
        model (type[T_PydanticModel] | None): Optional Pydantic model class for validation.
        strict (bool | None): Whether to use strict validation mode.
        context (Any | None): Additional context for validation.
        by_alias (bool | None): Whether to use field aliases during validation.
        by_name (bool | None): Whether to use field names during validation.
        n (int | None): Maximum number of objects to yield. ``None`` yields all.

    Yields:
        Any | T_PydanticModel: Parsed objects or validated Pydantic model instances.
    """
    count = 0
    for line in _iter_lines(data):
        if n is not None and count >= n:
            return
        if model is None:
            yield orjson.loads(line)
        else:
            yield model.model_validate_json(
                json_data=line,
                strict=strict,
                context=context,
                by_alias=by_alias,
                by_name=by_name,
            )
        count += 1


@overload
def iter_read(
    file: str | Path,
    /,
    *,
    n: int | None = None,
) -> Iterator[Any]: ...
@overload
def iter_read(
    file: str | Path,
    model: type[T_PydanticModel],
    /,
    strict: bool | None = None,
    context: Any | None = None,
    by_alias: bool | None = None,
    by_name: bool | None = None,
    *,
    n: int | None = None,
) -> Iterator[T_PydanticModel]: ...
def iter_read(
    file: str | Path,
    model: type[T_PydanticModel] | None = None,
    /,
    strict: bool | None = None,
    context: Any | None = None,
    by_alias: bool | None = None,
    by_name: bool | None = None,
    *,
    n: int | None = None,
) -> Iterator[Any] | Iterator[T_PydanticModel]:
    """
    Reads a JSONL file and lazily yields one parsed object per line.

    When no model is provided, each line is parsed into standard Python types.
    When a model is provided, each line is validated against the Pydantic model.

    Args:
        file (str | Path): Path to the JSONL file to be read.
        model (type[T_PydanticModel] | None): Optional Pydantic model class for validation.
        strict (bool | None): Whether to use strict validation mode.
        context (Any | None): Additional context for validation.
        by_alias (bool | None): Whether to use field aliases during validation.
        by_name (bool | None): Whether to use field names during validation.
        n (int | None): Maximum number of objects to yield. ``None`` yields all.

    Yields:
        Any | T_PydanticModel: Parsed objects or validated Pydantic model instances.
    """
    content: bytes = io.read_binary(file)
    yield from iter_parse(
        content,
        model,  # type: ignore
        strict=strict,
        context=context,
        by_alias=by_alias,
        by_name=by_name,
        n=n,
    )


@overload
def parse(
    data: str | bytes,
    /,
    *,
    n: int | None = None,
) -> list[Any]: ...
@overload
def parse(
    data: str | bytes,
    model: type[T_PydanticModel],
    /,
    strict: bool | None = None,
    context: Any | None = None,
    by_alias: bool | None = None,
    by_name: bool | None = None,
    *,
    n: int | None = None,
) -> list[T_PydanticModel]: ...
def parse(
    data: str | bytes,
    model: type[T_PydanticModel] | None = None,
    /,
    strict: bool | None = None,
    context: Any | None = None,
    by_alias: bool | None = None,
    by_name: bool | None = None,
    *,
    n: int | None = None,
) -> list[Any] | list[T_PydanticModel]:
    """
    Parses JSONL data into a list of Python objects or validated Pydantic models.

    When no model is provided, each line is parsed into standard Python types.
    When a model is provided, each line is validated against the Pydantic model.

    Args:
        data (str | bytes): JSONL data as string or bytes to be parsed.
        model (type[T_PydanticModel] | None): Optional Pydantic model class for validation.
        strict (bool | None): Whether to use strict validation mode.
        context (Any | None): Additional context for validation.
        by_alias (bool | None): Whether to use field aliases during validation.
        by_name (bool | None): Whether to use field names during validation.
        n (int | None): Maximum number of objects to return. ``None`` returns all.

    Returns:
        list[Any] | list[T_PydanticModel]: List of parsed objects or validated
            Pydantic model instances.
    """
    return list(
        iter_parse(
            data,
            model,  # type: ignore
            strict=strict,
            context=context,
            by_alias=by_alias,
            by_name=by_name,
            n=n,
        )
    )


@overload
def read(
    file: str | Path,
    /,
    *,
    n: int | None = None,
) -> list[Any]: ...
@overload
def read(
    file: str | Path,
    model: type[T_PydanticModel],
    /,
    strict: bool | None = None,
    context: Any | None = None,
    by_alias: bool | None = None,
    by_name: bool | None = None,
    *,
    n: int | None = None,
) -> list[T_PydanticModel]: ...
def read(
    file: str | Path,
    model: type[T_PydanticModel] | None = None,
    /,
    strict: bool | None = None,
    context: Any | None = None,
    by_alias: bool | None = None,
    by_name: bool | None = None,
    *,
    n: int | None = None,
) -> list[Any] | list[T_PydanticModel]:
    """
    Reads and parses a JSONL file into a list of Python objects or validated Pydantic models.

    When no model is provided, each line is parsed into standard Python types.
    When a model is provided, each line is validated against the Pydantic model.

    Args:
        file (str | Path): Path to the JSONL file to be read.
        model (type[T_PydanticModel] | None): Optional Pydantic model class for validation.
        strict (bool | None): Whether to use strict validation mode.
        context (Any | None): Additional context for validation.
        by_alias (bool | None): Whether to use field aliases during validation.
        by_name (bool | None): Whether to use field names during validation.
        n (int | None): Maximum number of objects to return. ``None`` returns all.

    Returns:
        list[Any] | list[T_PydanticModel]: List of parsed objects or validated
            Pydantic model instances.
    """
    content: bytes = io.read_binary(file)
    return parse(
        content,
        model,  # type: ignore
        strict=strict,
        context=context,
        by_alias=by_alias,
        by_name=by_name,
        n=n,
    )


def serialize(
    data: Iterable[JsonSerializable],
    returns: type[AnyStr] = str,
    encoding: str = "utf-8",
    fallback: Callable[[Any], Any] | None = None,
) -> AnyStr:
    """
    Serializes an iterable of objects to JSONL format.

    Each object in the iterable is serialized as a single JSON line.
    Automatically detects Pydantic models and routes to the appropriate
    serializer.

    Args:
        data (Iterable[JsonSerializable]): Objects to serialize, one per line.
        returns (type[AnyStr]): Return type, either ``str`` or ``bytes``.
        encoding (str): Character encoding for string output.
        fallback (Callable[[Any], Any] | None): Function to handle non-serializable objects.

    Returns:
        AnyStr: JSONL data as string or bytes based on *returns* parameter.

    Raises:
        TypeError: If *returns* is not ``bytes`` or ``str``.
    """
    lines: list[bytes] = [_serialize_one(obj, fallback) for obj in data]
    ser_data: bytes = b"\n".join(lines)
    if lines:
        ser_data += b"\n"

    if returns is bytes:
        return cast(AnyStr, ser_data)
    elif returns is str:
        return cast(AnyStr, ser_data.decode(encoding))
    else:
        raise TypeError(returns)


def write(
    file: str | Path,
    data: Iterable[JsonSerializable],
    overwrite: bool = False,
    fallback: Callable[[Any], Any] | None = None,
) -> None:
    """
    Writes an iterable of objects to a JSONL file.

    Each object in the iterable is serialized as a single JSON line.
    Automatically detects Pydantic models and routes to the appropriate
    serializer.

    Args:
        file (str | Path): Path to the output file.
        data (Iterable[JsonSerializable]): Objects to serialize, one per line.
        overwrite (bool): Whether to overwrite an existing file.
        fallback (Callable[[Any], Any] | None): Function to handle non-serializable objects.

    Returns:
        None
    """
    ser_data: bytes = serialize(data, returns=bytes, fallback=fallback)
    io.write_binary(file, ser_data, overwrite=overwrite)


def append(
    file: str | Path,
    data: JsonSerializable,
    fallback: Callable[[Any], Any] | None = None,
) -> None:
    """
    Appends a single JSON object as a new line to an existing JSONL file.

    If the file already exists and does not end with a newline character,
    one is inserted before the appended data to maintain valid JSONL format.
    If the file does not exist it is created.

    Args:
        file (str | Path): Path to the JSONL file.
        data (JsonSerializable): A single object to serialize and append.
        fallback (Callable[[Any], Any] | None): Function to handle non-serializable objects.

    Returns:
        None
    """
    path = Path(file)
    line: bytes = _serialize_one(data, fallback)

    if path.exists() and path.stat().st_size > 0:
        with open(path, "rb+") as fh:
            fh.seek(-1, 2)  # seek to last byte
            needs_newline = fh.read(1) != b"\n"
        with open(path, "ab") as fh:
            if needs_newline:
                fh.write(b"\n")
            fh.write(line)
            fh.write(b"\n")
    else:
        with open(path, "wb") as fh:
            fh.write(line)
            fh.write(b"\n")


def extend(
    file: str | Path,
    data: Iterable[JsonSerializable],
    fallback: Callable[[Any], Any] | None = None,
) -> None:
    """
    Extends a JSONL file with multiple JSON objects, one per line.

    If the file already exists and does not end with a newline character,
    one is inserted before the new data to maintain valid JSONL format.
    If the file does not exist it is created.

    Args:
        file (str | Path): Path to the JSONL file.
        data (Iterable[JsonSerializable]): Objects to serialize and append.
        fallback (Callable[[Any], Any] | None): Function to handle non-serializable objects.

    Returns:
        None
    """
    path = Path(file)
    lines: list[bytes] = [_serialize_one(obj, fallback) for obj in data]
    if not lines:
        return

    payload: bytes = b"\n".join(lines) + b"\n"

    if path.exists() and path.stat().st_size > 0:
        with open(path, "rb+") as fh:
            fh.seek(-1, 2)
            needs_newline = fh.read(1) != b"\n"
        with open(path, "ab") as fh:
            if needs_newline:
                fh.write(b"\n")
            fh.write(payload)
    else:
        with open(path, "wb") as fh:
            fh.write(payload)
