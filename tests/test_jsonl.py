from __future__ import annotations

from pathlib import Path
from typing import Any

import orjson
import pytest
from pydantic import BaseModel, Field, ValidationError

from pyeio.jsonl._jsonl import (
    _iter_lines,
    _serialize_one,
    append,
    extend,
    iter_parse,
    iter_read,
    parse,
    read,
    serialize,
    write,
)


class SimpleModel(BaseModel):
    name: str
    value: int


class NestedModel(BaseModel):
    id: int
    data: SimpleModel
    tags: list[str] = Field(default_factory=list)


class ModelWithAlias(BaseModel):
    field_name: str = Field(alias="fieldName")

    model_config = {"populate_by_name": True}


class ModelWithOptional(BaseModel):
    required: str
    optional: str | None = None
    with_default: str = "default_value"


@pytest.fixture
def simple_dicts() -> list[dict[str, Any]]:
    return [
        {"name": "alice", "value": 1},
        {"name": "bob", "value": 2},
        {"name": "charlie", "value": 3},
    ]


@pytest.fixture
def simple_jsonl_str() -> str:
    return '{"name":"alice","value":1}\n{"name":"bob","value":2}\n{"name":"charlie","value":3}\n'


@pytest.fixture
def simple_jsonl_bytes(simple_jsonl_str: str) -> bytes:
    return simple_jsonl_str.encode("utf-8")


@pytest.fixture
def simple_models() -> list[SimpleModel]:
    return [
        SimpleModel(name="alice", value=1),
        SimpleModel(name="bob", value=2),
        SimpleModel(name="charlie", value=3),
    ]


@pytest.fixture
def temp_jsonl_file(tmp_path: Path) -> Path:
    return tmp_path / "test.jsonl"


@pytest.fixture
def existing_jsonl_file(tmp_path: Path) -> Path:
    file = tmp_path / "existing.jsonl"
    file.write_bytes(b'{"existing":true}\n')
    return file


@pytest.fixture
def existing_jsonl_file_no_trailing_newline(tmp_path: Path) -> Path:
    file = tmp_path / "no_newline.jsonl"
    file.write_bytes(b'{"existing":true}')
    return file


class TestIterLines:
    def test_from_string(self):
        """Test yielding lines from a string."""
        lines = list(_iter_lines('{"a":1}\n{"b":2}\n'))
        assert lines == [b'{"a":1}', b'{"b":2}']

    def test_from_bytes(self):
        """Test yielding lines from bytes."""
        lines = list(_iter_lines(b'{"a":1}\n{"b":2}\n'))
        assert lines == [b'{"a":1}', b'{"b":2}']

    def test_skips_empty_lines(self):
        """Test that blank lines are skipped."""
        lines = list(_iter_lines(b'{"a":1}\n\n\n{"b":2}\n'))
        assert lines == [b'{"a":1}', b'{"b":2}']

    def test_strips_whitespace(self):
        """Test that leading/trailing whitespace is stripped from lines."""
        lines = list(_iter_lines(b'  {"a":1}  \n  {"b":2}  \n'))
        assert lines == [b'{"a":1}', b'{"b":2}']

    def test_empty_input(self):
        """Test that empty input yields nothing."""
        assert list(_iter_lines(b"")) == []
        assert list(_iter_lines("")) == []

    def test_no_trailing_newline(self):
        """Test input without trailing newline."""
        lines = list(_iter_lines(b'{"a":1}\n{"b":2}'))
        assert lines == [b'{"a":1}', b'{"b":2}']

    def test_invalid_type_raises_error(self):
        """Test that non-str/bytes input raises TypeError."""
        with pytest.raises(TypeError):
            list(_iter_lines(12345))  # type: ignore


class TestSerializeOne:
    def test_serialize_dict(self):
        """Test serializing a plain dict."""
        result = _serialize_one({"a": 1})
        assert isinstance(result, bytes)
        assert orjson.loads(result) == {"a": 1}

    def test_serialize_list(self):
        """Test serializing a list."""
        result = _serialize_one([1, 2, 3])
        assert orjson.loads(result) == [1, 2, 3]

    def test_serialize_pydantic_model(self):
        """Test serializing a Pydantic model."""
        model = SimpleModel(name="test", value=42)
        result = _serialize_one(model)
        assert isinstance(result, bytes)
        parsed = orjson.loads(result)
        assert parsed == {"name": "test", "value": 42}

    def test_serialize_with_fallback(self):
        """Test serializing with a fallback function."""

        class Custom:
            def __init__(self, v: int):
                self.v = v

        def fallback(obj: Any) -> Any:
            if isinstance(obj, Custom):
                return {"custom": obj.v}
            raise TypeError

        result = _serialize_one({"obj": Custom(7)}, fallback=fallback)
        assert orjson.loads(result) == {"obj": {"custom": 7}}

    def test_no_trailing_newline(self):
        """Test that the output never contains a trailing newline."""
        result = _serialize_one({"a": 1})
        assert not result.endswith(b"\n")


class TestIterParse:
    def test_parse_string_without_model(
        self, simple_jsonl_str: str, simple_dicts: list[dict]
    ):
        """Test lazily parsing JSONL string into dicts."""
        result = list(iter_parse(simple_jsonl_str))
        assert result == simple_dicts

    def test_parse_bytes_without_model(
        self, simple_jsonl_bytes: bytes, simple_dicts: list[dict]
    ):
        """Test lazily parsing JSONL bytes into dicts."""
        result = list(iter_parse(simple_jsonl_bytes))
        assert result == simple_dicts

    def test_parse_with_pydantic_model(self, simple_jsonl_bytes: bytes):
        """Test lazily parsing JSONL into Pydantic models."""
        result = list(iter_parse(simple_jsonl_bytes, SimpleModel))
        assert all(isinstance(r, SimpleModel) for r in result)
        assert result[0].name == "alice"
        assert result[2].value == 3

    def test_n_limits_output(self, simple_jsonl_bytes: bytes):
        """Test that n limits the number of yielded objects."""
        result = list(iter_parse(simple_jsonl_bytes, n=2))
        assert len(result) == 2
        assert result[0] == {"name": "alice", "value": 1}
        assert result[1] == {"name": "bob", "value": 2}

    def test_n_limits_output_with_model(self, simple_jsonl_bytes: bytes):
        """Test that n limits the number of yielded Pydantic models."""
        result = list(iter_parse(simple_jsonl_bytes, SimpleModel, n=1))
        assert len(result) == 1
        assert isinstance(result[0], SimpleModel)
        assert result[0].name == "alice"

    def test_n_none_yields_all(self, simple_jsonl_bytes: bytes):
        """Test that n=None yields all objects."""
        result = list(iter_parse(simple_jsonl_bytes, n=None))
        assert len(result) == 3

    def test_n_zero_yields_nothing(self, simple_jsonl_bytes: bytes):
        """Test that n=0 yields no objects."""
        result = list(iter_parse(simple_jsonl_bytes, n=0))
        assert result == []

    def test_n_greater_than_lines(self, simple_jsonl_bytes: bytes):
        """Test that n larger than line count yields all objects."""
        result = list(iter_parse(simple_jsonl_bytes, n=100))
        assert len(result) == 3

    def test_empty_input(self):
        """Test parsing empty input."""
        result = list(iter_parse(b""))
        assert result == []

    def test_single_line(self):
        """Test parsing a single-line JSONL."""
        result = list(iter_parse(b'{"a":1}\n'))
        assert result == [{"a": 1}]

    def test_strict_mode(self, simple_jsonl_bytes: bytes):
        """Test parsing with strict validation mode."""
        result = list(iter_parse(simple_jsonl_bytes, SimpleModel, strict=True))
        assert len(result) == 3

    def test_context(self, simple_jsonl_bytes: bytes):
        """Test parsing with validation context."""
        result = list(
            iter_parse(simple_jsonl_bytes, SimpleModel, context={"extra": "ctx"})
        )
        assert len(result) == 3

    def test_by_alias(self):
        """Test parsing with by_alias option."""
        data = b'{"fieldName":"test"}\n'
        result = list(iter_parse(data, ModelWithAlias, by_alias=True))
        assert result[0].field_name == "test"

    def test_by_name(self):
        """Test parsing with by_name option."""
        data = b'{"field_name":"test"}\n'
        result = list(iter_parse(data, ModelWithAlias, by_name=True))
        assert result[0].field_name == "test"

    def test_invalid_json_raises_error(self):
        """Test that an invalid JSON line raises an error."""
        with pytest.raises(orjson.JSONDecodeError):
            list(iter_parse(b"{bad json}\n"))

    def test_pydantic_validation_error(self):
        """Test that invalid data raises a Pydantic validation error."""
        data = b'{"name":"test"}\n'  # missing 'value'
        with pytest.raises(ValidationError):
            list(iter_parse(data, SimpleModel))

    def test_is_lazy(self, simple_jsonl_bytes: bytes):
        """Test that iter_parse returns an iterator, not a list."""
        result = iter_parse(simple_jsonl_bytes)
        assert hasattr(result, "__next__")


class TestIterRead:
    def test_read_without_model(self, tmp_path: Path, simple_dicts: list[dict]):
        """Test lazily reading JSONL file into dicts."""
        file = tmp_path / "test.jsonl"
        file.write_bytes(
            b'{"name":"alice","value":1}\n{"name":"bob","value":2}\n{"name":"charlie","value":3}\n'
        )
        result = list(iter_read(file))
        assert result == simple_dicts

    def test_read_with_string_path(self, tmp_path: Path):
        """Test reading with a string path."""
        file = tmp_path / "test.jsonl"
        file.write_bytes(b'{"a":1}\n')
        result = list(iter_read(str(file)))
        assert result == [{"a": 1}]

    def test_read_with_pydantic_model(self, tmp_path: Path):
        """Test lazily reading JSONL into Pydantic models."""
        file = tmp_path / "test.jsonl"
        file.write_bytes(b'{"name":"alice","value":1}\n{"name":"bob","value":2}\n')
        result = list(iter_read(file, SimpleModel))
        assert all(isinstance(r, SimpleModel) for r in result)
        assert result[0].name == "alice"
        assert result[1].value == 2

    def test_n_limits_output(self, tmp_path: Path):
        """Test that n limits the number of yielded objects from file."""
        file = tmp_path / "test.jsonl"
        file.write_bytes(b'{"a":1}\n{"a":2}\n{"a":3}\n')
        result = list(iter_read(file, n=2))
        assert len(result) == 2

    def test_nonexistent_file_raises_error(self, tmp_path: Path):
        """Test that reading a non-existent file raises FileNotFoundError."""
        with pytest.raises(FileNotFoundError):
            list(iter_read(tmp_path / "missing.jsonl"))

    def test_empty_file(self, tmp_path: Path):
        """Test reading an empty file."""
        file = tmp_path / "empty.jsonl"
        file.write_bytes(b"")
        result = list(iter_read(file))
        assert result == []

    def test_is_lazy(self, tmp_path: Path):
        """Test that iter_read returns an iterator."""
        file = tmp_path / "test.jsonl"
        file.write_bytes(b'{"a":1}\n')
        result = iter_read(file)
        assert hasattr(result, "__next__")


class TestParse:
    def test_parse_string_without_model(
        self, simple_jsonl_str: str, simple_dicts: list[dict]
    ):
        """Test parsing JSONL string into a list of dicts."""
        result = parse(simple_jsonl_str)
        assert result == simple_dicts

    def test_parse_bytes_without_model(
        self, simple_jsonl_bytes: bytes, simple_dicts: list[dict]
    ):
        """Test parsing JSONL bytes into a list of dicts."""
        result = parse(simple_jsonl_bytes)
        assert result == simple_dicts

    def test_parse_with_pydantic_model(self, simple_jsonl_bytes: bytes):
        """Test parsing JSONL into a list of Pydantic models."""
        result = parse(simple_jsonl_bytes, SimpleModel)
        assert isinstance(result, list)
        assert all(isinstance(r, SimpleModel) for r in result)
        assert len(result) == 3
        assert result[1].name == "bob"

    def test_parse_nested_model(self):
        """Test parsing JSONL into nested Pydantic models."""
        data = b'{"id":1,"data":{"name":"a","value":10},"tags":["x"]}\n{"id":2,"data":{"name":"b","value":20},"tags":[]}\n'
        result = parse(data, NestedModel)
        assert len(result) == 2
        assert result[0].data.name == "a"
        assert result[1].tags == []

    def test_n_limits_output(self, simple_jsonl_bytes: bytes):
        """Test that n limits the returned list length."""
        result = parse(simple_jsonl_bytes, n=1)
        assert len(result) == 1

    def test_n_none_returns_all(self, simple_jsonl_bytes: bytes):
        """Test that n=None returns all objects."""
        result = parse(simple_jsonl_bytes, n=None)
        assert len(result) == 3

    def test_returns_list(self, simple_jsonl_bytes: bytes):
        """Test that parse always returns a list, not an iterator."""
        result = parse(simple_jsonl_bytes)
        assert isinstance(result, list)

    def test_empty_input(self):
        """Test parsing empty input returns empty list."""
        assert parse(b"") == []
        assert parse("") == []

    def test_single_line(self):
        """Test parsing single-line JSONL."""
        result = parse(b'{"x":99}\n')
        assert result == [{"x": 99}]

    def test_strict_mode(self, simple_jsonl_bytes: bytes):
        """Test parsing with strict validation mode."""
        result = parse(simple_jsonl_bytes, SimpleModel, strict=True)
        assert len(result) == 3

    def test_by_alias(self):
        """Test parsing with by_alias option."""
        data = b'{"fieldName":"one"}\n{"fieldName":"two"}\n'
        result = parse(data, ModelWithAlias, by_alias=True)
        assert [r.field_name for r in result] == ["one", "two"]

    def test_by_name(self):
        """Test parsing with by_name option."""
        data = b'{"field_name":"one"}\n'
        result = parse(data, ModelWithAlias, by_name=True)
        assert result[0].field_name == "one"

    def test_invalid_json_raises_error(self):
        """Test that invalid JSON raises JSONDecodeError."""
        with pytest.raises(orjson.JSONDecodeError):
            parse(b"not json\n")

    def test_pydantic_validation_error(self):
        """Test that invalid data raises Pydantic ValidationError."""
        data = b'{"name":"ok","value":1}\n{"name":"bad"}\n'
        with pytest.raises(ValidationError):
            parse(data, SimpleModel)

    def test_primitive_lines(self):
        """Test parsing lines that are JSON primitives."""
        data = b"1\n2\n3\n"
        result = parse(data)
        assert result == [1, 2, 3]

    def test_mixed_types(self):
        """Test parsing lines with mixed JSON types."""
        data = b'{"a":1}\n[1,2]\n"hello"\nnull\ntrue\n42\n'
        result = parse(data)
        assert result == [{"a": 1}, [1, 2], "hello", None, True, 42]


class TestRead:
    def test_read_without_model(self, tmp_path: Path, simple_dicts: list[dict]):
        """Test reading JSONL file into list of dicts."""
        file = tmp_path / "test.jsonl"
        file.write_bytes(
            b'{"name":"alice","value":1}\n{"name":"bob","value":2}\n{"name":"charlie","value":3}\n'
        )
        result = read(file)
        assert result == simple_dicts

    def test_read_with_string_path(self, tmp_path: Path):
        """Test reading with a string path."""
        file = tmp_path / "test.jsonl"
        file.write_bytes(b'{"k":"v"}\n')
        result = read(str(file))
        assert result == [{"k": "v"}]

    def test_read_with_pydantic_model(self, tmp_path: Path):
        """Test reading JSONL into Pydantic models."""
        file = tmp_path / "test.jsonl"
        file.write_bytes(b'{"name":"alice","value":1}\n{"name":"bob","value":2}\n')
        result = read(file, SimpleModel)
        assert isinstance(result, list)
        assert all(isinstance(r, SimpleModel) for r in result)

    def test_n_limits_output(self, tmp_path: Path):
        """Test that n limits the returned list length from file."""
        file = tmp_path / "test.jsonl"
        file.write_bytes(b'{"a":1}\n{"a":2}\n{"a":3}\n')
        result = read(file, n=2)
        assert len(result) == 2

    def test_nonexistent_file_raises_error(self, tmp_path: Path):
        """Test that reading a non-existent file raises FileNotFoundError."""
        with pytest.raises(FileNotFoundError):
            read(tmp_path / "missing.jsonl")

    def test_invalid_json_raises_error(self, tmp_path: Path):
        """Test that invalid JSON in file raises JSONDecodeError."""
        file = tmp_path / "bad.jsonl"
        file.write_bytes(b"{not valid}\n")
        with pytest.raises(orjson.JSONDecodeError):
            read(file)

    def test_empty_file(self, tmp_path: Path):
        """Test reading an empty file returns empty list."""
        file = tmp_path / "empty.jsonl"
        file.write_bytes(b"")
        assert read(file) == []

    def test_returns_list(self, tmp_path: Path):
        """Test that read returns a list."""
        file = tmp_path / "test.jsonl"
        file.write_bytes(b'{"a":1}\n')
        result = read(file)
        assert isinstance(result, list)

    def test_strict_mode(self, tmp_path: Path):
        """Test reading with strict validation mode."""
        file = tmp_path / "test.jsonl"
        file.write_bytes(b'{"name":"x","value":1}\n')
        result = read(file, SimpleModel, strict=True)
        assert len(result) == 1

    def test_context(self, tmp_path: Path):
        """Test reading with validation context."""
        file = tmp_path / "test.jsonl"
        file.write_bytes(b'{"name":"x","value":1}\n')
        result = read(file, SimpleModel, context={"key": "val"})
        assert len(result) == 1


class TestSerialize:
    def test_serialize_dicts_to_str(self, simple_dicts: list[dict]):
        """Test serializing list of dicts to JSONL string (default)."""
        result = serialize(simple_dicts)
        assert isinstance(result, str)
        lines = [l for l in result.strip().split("\n") if l]
        assert len(lines) == 3
        assert orjson.loads(lines[0]) == simple_dicts[0]

    def test_serialize_dicts_to_bytes(self, simple_dicts: list[dict]):
        """Test serializing list of dicts to JSONL bytes."""
        result = serialize(simple_dicts, returns=bytes)
        assert isinstance(result, bytes)
        lines = [l for l in result.strip().split(b"\n") if l]
        assert len(lines) == 3

    def test_serialize_trailing_newline(self, simple_dicts: list[dict]):
        """Test that serialized output ends with a trailing newline."""
        result = serialize(simple_dicts, returns=bytes)
        assert result.endswith(b"\n")

    def test_serialize_pydantic_models(self, simple_models: list[SimpleModel]):
        """Test serializing list of Pydantic models."""
        result = serialize(simple_models, returns=bytes)
        lines = [l for l in result.strip().split(b"\n") if l]
        assert len(lines) == 3
        parsed = orjson.loads(lines[0])
        assert parsed == {"name": "alice", "value": 1}

    def test_serialize_mixed_pydantic_and_dicts(self):
        """Test serializing a mix of Pydantic models and dicts."""
        data: list[Any] = [
            SimpleModel(name="model", value=1),
            {"name": "dict", "value": 2},
        ]
        result = serialize(data, returns=bytes)
        lines = [l for l in result.strip().split(b"\n") if l]
        assert len(lines) == 2
        assert orjson.loads(lines[0]) == {"name": "model", "value": 1}
        assert orjson.loads(lines[1]) == {"name": "dict", "value": 2}

    def test_serialize_empty_iterable(self):
        """Test serializing an empty iterable produces empty bytes."""
        result_bytes = serialize([], returns=bytes)
        assert result_bytes == b""
        result_str = serialize([], returns=str)
        assert result_str == ""

    def test_serialize_single_item(self):
        """Test serializing a single-item iterable."""
        result = serialize([{"a": 1}], returns=bytes)
        assert result == b'{"a":1}\n'

    def test_serialize_with_fallback(self):
        """Test serializing with a fallback function."""

        class Custom:
            def __init__(self, v: int):
                self.v = v

        def fallback(obj: Any) -> Any:
            if isinstance(obj, Custom):
                return {"custom": obj.v}
            raise TypeError

        result = serialize([{"obj": Custom(5)}], returns=bytes, fallback=fallback)
        parsed = orjson.loads(result.strip())
        assert parsed == {"obj": {"custom": 5}}

    def test_serialize_with_encoding(self, simple_dicts: list[dict]):
        """Test serializing with custom encoding."""
        result = serialize(simple_dicts, returns=str, encoding="utf-8")
        assert isinstance(result, str)

    def test_serialize_invalid_returns_type_raises_error(
        self, simple_dicts: list[dict]
    ):
        """Test that invalid returns type raises TypeError."""
        with pytest.raises(TypeError):
            serialize(simple_dicts, returns=list)  # type: ignore

    def test_serialize_generator(self):
        """Test serializing from a generator (non-list iterable)."""

        def gen():
            yield {"a": 1}
            yield {"b": 2}

        result = serialize(gen(), returns=bytes)
        lines = [l for l in result.strip().split(b"\n") if l]
        assert len(lines) == 2

    def test_serialize_roundtrip(self, simple_dicts: list[dict]):
        """Test that serialized data can be parsed back."""
        serialized = serialize(simple_dicts, returns=bytes)
        parsed = parse(serialized)
        assert parsed == simple_dicts


class TestWrite:
    def test_write_dicts(self, temp_jsonl_file: Path, simple_dicts: list[dict]):
        """Test writing list of dicts to JSONL file."""
        write(temp_jsonl_file, simple_dicts)
        assert temp_jsonl_file.exists()
        result = parse(temp_jsonl_file.read_bytes())
        assert result == simple_dicts

    def test_write_with_string_path(self, temp_jsonl_file: Path):
        """Test writing with string path."""
        write(str(temp_jsonl_file), [{"a": 1}])
        assert temp_jsonl_file.exists()

    def test_write_pydantic_models(
        self, temp_jsonl_file: Path, simple_models: list[SimpleModel]
    ):
        """Test writing list of Pydantic models."""
        write(temp_jsonl_file, simple_models)
        result = parse(temp_jsonl_file.read_bytes(), SimpleModel)
        assert result == simple_models

    def test_write_empty_iterable(self, temp_jsonl_file: Path):
        """Test writing an empty iterable creates an empty file."""
        write(temp_jsonl_file, [])
        assert temp_jsonl_file.exists()
        assert temp_jsonl_file.read_bytes() == b""

    def test_write_overwrite_false_raises_on_existing(
        self,
        existing_jsonl_file: Path,
    ):
        """Test that overwrite=False raises error for existing file."""
        with pytest.raises(FileExistsError):
            write(existing_jsonl_file, [{"new": True}], overwrite=False)

    def test_write_overwrite_true_replaces_existing(
        self,
        existing_jsonl_file: Path,
    ):
        """Test that overwrite=True replaces existing file content."""
        write(existing_jsonl_file, [{"new": True}], overwrite=True)
        result = parse(existing_jsonl_file.read_bytes())
        assert result == [{"new": True}]

    def test_write_with_fallback(self, temp_jsonl_file: Path):
        """Test writing with a fallback function."""

        class Custom:
            def __init__(self, v: int):
                self.v = v

        def fallback(obj: Any) -> Any:
            if isinstance(obj, Custom):
                return obj.v
            raise TypeError

        write(temp_jsonl_file, [{"val": Custom(9)}], fallback=fallback)
        result = parse(temp_jsonl_file.read_bytes())
        assert result == [{"val": 9}]

    def test_write_roundtrip(self, temp_jsonl_file: Path, simple_dicts: list[dict]):
        """Test that written file can be read back."""
        write(temp_jsonl_file, simple_dicts)
        result = read(temp_jsonl_file)
        assert result == simple_dicts

    def test_write_roundtrip_pydantic(
        self, temp_jsonl_file: Path, simple_models: list[SimpleModel]
    ):
        """Test Pydantic model write/read roundtrip."""
        write(temp_jsonl_file, simple_models)
        result = read(temp_jsonl_file, SimpleModel)
        assert result == simple_models


class TestAppend:
    def test_append_to_existing_file(self, existing_jsonl_file: Path):
        """Test appending a single object to an existing file."""
        append(existing_jsonl_file, {"appended": True})
        result = parse(existing_jsonl_file.read_bytes())
        assert len(result) == 2
        assert result[0] == {"existing": True}
        assert result[1] == {"appended": True}

    def test_append_creates_new_file(self, temp_jsonl_file: Path):
        """Test that append creates the file if it does not exist."""
        assert not temp_jsonl_file.exists()
        append(temp_jsonl_file, {"first": True})
        assert temp_jsonl_file.exists()
        result = parse(temp_jsonl_file.read_bytes())
        assert result == [{"first": True}]

    def test_append_adds_trailing_newline(self, temp_jsonl_file: Path):
        """Test that appended data ends with a newline."""
        append(temp_jsonl_file, {"a": 1})
        assert temp_jsonl_file.read_bytes().endswith(b"\n")

    def test_append_inserts_newline_when_missing(
        self, existing_jsonl_file_no_trailing_newline: Path
    ):
        """Test that a newline is inserted before appended data when file lacks one."""
        append(existing_jsonl_file_no_trailing_newline, {"appended": True})
        content = existing_jsonl_file_no_trailing_newline.read_bytes()
        result = parse(content)
        assert len(result) == 2
        assert result[0] == {"existing": True}
        assert result[1] == {"appended": True}
        # Verify no double newline
        assert b"\n\n" not in content

    def test_append_preserves_existing_trailing_newline(
        self, existing_jsonl_file: Path
    ):
        """Test that no extra newline is added when file already ends with one."""
        append(existing_jsonl_file, {"appended": True})
        content = existing_jsonl_file.read_bytes()
        assert b"\n\n" not in content

    def test_append_multiple_times(self, temp_jsonl_file: Path):
        """Test appending multiple objects one at a time."""
        for i in range(5):
            append(temp_jsonl_file, {"i": i})
        result = parse(temp_jsonl_file.read_bytes())
        assert len(result) == 5
        assert [r["i"] for r in result] == [0, 1, 2, 3, 4]

    def test_append_pydantic_model(self, temp_jsonl_file: Path):
        """Test appending a Pydantic model."""
        append(temp_jsonl_file, SimpleModel(name="test", value=42))
        result = parse(temp_jsonl_file.read_bytes(), SimpleModel)
        assert len(result) == 1
        assert result[0].name == "test"
        assert result[0].value == 42

    def test_append_to_empty_existing_file(self, tmp_path: Path):
        """Test appending to a file that exists but is empty (0 bytes)."""
        file = tmp_path / "empty.jsonl"
        file.write_bytes(b"")
        append(file, {"a": 1})
        result = parse(file.read_bytes())
        assert result == [{"a": 1}]

    def test_append_with_fallback(self, temp_jsonl_file: Path):
        """Test appending with a fallback function."""

        class Custom:
            def __init__(self, v: int):
                self.v = v

        def fallback(obj: Any) -> Any:
            if isinstance(obj, Custom):
                return obj.v
            raise TypeError

        append(temp_jsonl_file, {"val": Custom(7)}, fallback=fallback)
        result = parse(temp_jsonl_file.read_bytes())
        assert result == [{"val": 7}]

    def test_append_with_string_path(self, temp_jsonl_file: Path):
        """Test appending using a string path."""
        append(str(temp_jsonl_file), {"a": 1})
        assert temp_jsonl_file.exists()
        result = parse(temp_jsonl_file.read_bytes())
        assert result == [{"a": 1}]


# ── extend ───────────────────────────────────────────────────────────────────


class TestExtend:
    def test_extend_existing_file(self, existing_jsonl_file: Path):
        """Test extending an existing file with multiple objects."""
        extend(existing_jsonl_file, [{"a": 1}, {"b": 2}])
        result = parse(existing_jsonl_file.read_bytes())
        assert len(result) == 3
        assert result[0] == {"existing": True}
        assert result[1] == {"a": 1}
        assert result[2] == {"b": 2}

    def test_extend_creates_new_file(self, temp_jsonl_file: Path):
        """Test that extend creates the file if it does not exist."""
        assert not temp_jsonl_file.exists()
        extend(temp_jsonl_file, [{"a": 1}, {"b": 2}])
        assert temp_jsonl_file.exists()
        result = parse(temp_jsonl_file.read_bytes())
        assert result == [{"a": 1}, {"b": 2}]

    def test_extend_adds_trailing_newline(self, temp_jsonl_file: Path):
        """Test that extended data ends with a newline."""
        extend(temp_jsonl_file, [{"a": 1}])
        assert temp_jsonl_file.read_bytes().endswith(b"\n")

    def test_extend_inserts_newline_when_missing(
        self, existing_jsonl_file_no_trailing_newline: Path
    ):
        """Test that a newline is inserted when file lacks a trailing one."""
        extend(existing_jsonl_file_no_trailing_newline, [{"new": True}])
        content = existing_jsonl_file_no_trailing_newline.read_bytes()
        result = parse(content)
        assert len(result) == 2
        assert result[0] == {"existing": True}
        assert result[1] == {"new": True}
        assert b"\n\n" not in content

    def test_extend_preserves_existing_trailing_newline(
        self, existing_jsonl_file: Path
    ):
        """Test that no extra newline is added when file already ends with one."""
        extend(existing_jsonl_file, [{"new": True}])
        content = existing_jsonl_file.read_bytes()
        assert b"\n\n" not in content

    def test_extend_with_empty_iterable_is_noop(self, existing_jsonl_file: Path):
        """Test that extending with empty iterable does not modify the file."""
        original = existing_jsonl_file.read_bytes()
        extend(existing_jsonl_file, [])
        assert existing_jsonl_file.read_bytes() == original

    def test_extend_with_empty_iterable_no_create(self, temp_jsonl_file: Path):
        """Test that extending with empty iterable does not create a file."""
        extend(temp_jsonl_file, [])
        assert not temp_jsonl_file.exists()

    def test_extend_pydantic_models(self, temp_jsonl_file: Path):
        """Test extending with Pydantic models."""
        models = [
            SimpleModel(name="a", value=1),
            SimpleModel(name="b", value=2),
        ]
        extend(temp_jsonl_file, models)
        result = parse(temp_jsonl_file.read_bytes(), SimpleModel)
        assert result == models

    def test_extend_multiple_times(self, temp_jsonl_file: Path):
        """Test extending a file multiple times."""
        extend(temp_jsonl_file, [{"batch": 1, "i": i} for i in range(3)])
        extend(temp_jsonl_file, [{"batch": 2, "i": i} for i in range(2)])
        result = parse(temp_jsonl_file.read_bytes())
        assert len(result) == 5
        assert result[0]["batch"] == 1
        assert result[3]["batch"] == 2

    def test_extend_to_empty_existing_file(self, tmp_path: Path):
        """Test extending a file that exists but is empty."""
        file = tmp_path / "empty.jsonl"
        file.write_bytes(b"")
        extend(file, [{"a": 1}, {"b": 2}])
        result = parse(file.read_bytes())
        assert result == [{"a": 1}, {"b": 2}]

    def test_extend_with_fallback(self, temp_jsonl_file: Path):
        """Test extending with a fallback function."""

        class Custom:
            def __init__(self, v: int):
                self.v = v

        def fallback(obj: Any) -> Any:
            if isinstance(obj, Custom):
                return obj.v
            raise TypeError

        extend(
            temp_jsonl_file, [{"val": Custom(3)}, {"val": Custom(4)}], fallback=fallback
        )
        result = parse(temp_jsonl_file.read_bytes())
        assert result == [{"val": 3}, {"val": 4}]

    def test_extend_with_string_path(self, temp_jsonl_file: Path):
        """Test extending using a string path."""
        extend(str(temp_jsonl_file), [{"a": 1}])
        assert temp_jsonl_file.exists()

    def test_extend_with_generator(self, temp_jsonl_file: Path):
        """Test extending from a generator (non-list iterable)."""

        def gen():
            yield {"a": 1}
            yield {"a": 2}

        extend(temp_jsonl_file, gen())
        result = parse(temp_jsonl_file.read_bytes())
        assert len(result) == 2


# ── Edge Cases & Integration ─────────────────────────────────────────────────


class TestEdgeCases:
    def test_unicode_content(self, temp_jsonl_file: Path):
        """Test handling of unicode content."""
        data = [{"message": "Hello, 世界! 🌍"}, {"message": "café"}]
        write(temp_jsonl_file, data)
        result = read(temp_jsonl_file)
        assert result[0]["message"] == "Hello, 世界! 🌍"
        assert result[1]["message"] == "café"

    def test_deeply_nested_structure(self, temp_jsonl_file: Path):
        """Test deeply nested JSON objects."""
        data = [{"l1": {"l2": {"l3": {"value": "deep"}}}}]
        write(temp_jsonl_file, data)
        result = read(temp_jsonl_file)
        assert result[0]["l1"]["l2"]["l3"]["value"] == "deep"

    def test_large_number_of_lines(self, temp_jsonl_file: Path):
        """Test writing and reading a large number of lines."""
        n = 10_000
        data = [{"i": i} for i in range(n)]
        write(temp_jsonl_file, data)
        result = read(temp_jsonl_file)
        assert len(result) == n
        assert result[0]["i"] == 0
        assert result[-1]["i"] == n - 1

    def test_lines_with_special_characters(self):
        """Test parsing lines with escaped characters."""
        data = b'{"text":"line1\\nline2"}\n{"text":"tab\\there"}\n'
        result = parse(data)
        assert result[0]["text"] == "line1\nline2"
        assert result[1]["text"] == "tab\there"

    def test_numeric_keys_coerced_to_str(self):
        """Test that numeric dict keys are coerced to strings."""
        data = [{1: "one", 2: "two"}]
        result_bytes = serialize(data, returns=bytes)
        parsed = parse(result_bytes)
        assert parsed == [{"1": "one", "2": "two"}]

    def test_null_values(self):
        """Test handling of null JSON values."""
        data = b'{"a":null}\n'
        result = parse(data)
        assert result == [{"a": None}]

    def test_boolean_values(self):
        """Test handling of boolean JSON values."""
        data = b'{"t":true,"f":false}\n'
        result = parse(data)
        assert result == [{"t": True, "f": False}]

    def test_empty_objects_and_arrays(self):
        """Test handling of empty JSON objects and arrays."""
        data = b"{}\n[]\n"
        result = parse(data)
        assert result == [{}, []]

    def test_windows_line_endings(self):
        """Test that CRLF line endings are handled correctly."""
        data = b'{"a":1}\r\n{"b":2}\r\n'
        result = parse(data)
        assert result == [{"a": 1}, {"b": 2}]


class TestIntegration:
    def test_write_read_roundtrip_dicts(
        self, temp_jsonl_file: Path, simple_dicts: list[dict]
    ):
        """Test full write/read roundtrip with plain dicts."""
        write(temp_jsonl_file, simple_dicts)
        result = read(temp_jsonl_file)
        assert result == simple_dicts

    def test_write_read_roundtrip_pydantic(
        self, temp_jsonl_file: Path, simple_models: list[SimpleModel]
    ):
        """Test full write/read roundtrip with Pydantic models."""
        write(temp_jsonl_file, simple_models)
        result = read(temp_jsonl_file, SimpleModel)
        assert result == simple_models

    def test_serialize_parse_roundtrip(self, simple_dicts: list[dict]):
        """Test serialize/parse roundtrip in memory."""
        serialized = serialize(simple_dicts, returns=bytes)
        parsed = parse(serialized)
        assert parsed == simple_dicts

    def test_append_then_read(self, temp_jsonl_file: Path):
        """Test appending objects one by one then reading them all."""
        items = [{"x": i} for i in range(5)]
        for item in items:
            append(temp_jsonl_file, item)
        result = read(temp_jsonl_file)
        assert result == items

    def test_write_then_extend_then_read(self, temp_jsonl_file: Path):
        """Test writing initial data, extending, then reading."""
        write(temp_jsonl_file, [{"batch": 0}])
        extend(temp_jsonl_file, [{"batch": 1}, {"batch": 2}])
        result = read(temp_jsonl_file)
        assert len(result) == 3
        assert [r["batch"] for r in result] == [0, 1, 2]

    def test_write_then_append_then_extend_then_read(self, temp_jsonl_file: Path):
        """Test combining write, append, and extend operations."""
        write(temp_jsonl_file, [{"op": "write"}])
        append(temp_jsonl_file, {"op": "append"})
        extend(temp_jsonl_file, [{"op": "extend1"}, {"op": "extend2"}])
        result = read(temp_jsonl_file)
        assert len(result) == 4
        assert [r["op"] for r in result] == ["write", "append", "extend1", "extend2"]

    def test_iter_read_partial_then_read_full(self, tmp_path: Path):
        """Test lazily reading a subset then reading all."""
        file = tmp_path / "test.jsonl"
        data = [{"i": i} for i in range(10)]
        write(file, data)

        partial = list(iter_read(file, n=3))
        assert len(partial) == 3

        full = read(file)
        assert len(full) == 10

    def test_mixed_model_and_dict_append(self, temp_jsonl_file: Path):
        """Test appending both dicts and Pydantic models to the same file."""
        append(temp_jsonl_file, {"raw": True})
        append(temp_jsonl_file, SimpleModel(name="model", value=99))
        result = read(temp_jsonl_file)
        assert len(result) == 2
        assert result[0] == {"raw": True}
        assert result[1] == {"name": "model", "value": 99}
