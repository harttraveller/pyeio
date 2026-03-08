from __future__ import annotations

import pytest


@pytest.fixture(autouse=True)
def _clean_pyeio_cache():
    """
    Ensure each test exercises ``__getattr__`` from scratch by removing
    cached dynamic attributes from the ``pyeio`` module globals between tests.
    """
    import pyeio

    yield
    for name in ("json", "toml", "yaml", "jsonl", "yml", "ndjson"):
        pyeio.__dict__.pop(name, None)


class TestStaticImports:
    def test_open(self):
        """Test that open is re-exported from builtins."""
        from pyeio import open as pyeio_open

        assert pyeio_open is open

    def test_io_constants(self):
        """Test that io constants are re-exported."""
        import io

        from pyeio import DEFAULT_BUFFER_SIZE, SEEK_CUR, SEEK_END, SEEK_SET

        assert DEFAULT_BUFFER_SIZE == io.DEFAULT_BUFFER_SIZE
        assert SEEK_SET == io.SEEK_SET
        assert SEEK_CUR == io.SEEK_CUR
        assert SEEK_END == io.SEEK_END

    def test_io_classes(self):
        """Test that io classes are re-exported."""
        import io

        from pyeio import (
            BufferedIOBase,
            BufferedRandom,
            BufferedReader,
            BufferedRWPair,
            BufferedWriter,
            BytesIO,
            FileIO,
            IOBase,
            RawIOBase,
            StringIO,
            TextIOBase,
            TextIOWrapper,
        )

        assert BufferedIOBase is io.BufferedIOBase
        assert BufferedRandom is io.BufferedRandom
        assert BufferedReader is io.BufferedReader
        assert BufferedRWPair is io.BufferedRWPair
        assert BufferedWriter is io.BufferedWriter
        assert BytesIO is io.BytesIO
        assert FileIO is io.FileIO
        assert IOBase is io.IOBase
        assert RawIOBase is io.RawIOBase
        assert StringIO is io.StringIO
        assert TextIOBase is io.TextIOBase
        assert TextIOWrapper is io.TextIOWrapper

    def test_io_utilities(self):
        """Test that io utility functions are re-exported."""
        import io

        from pyeio import (
            BlockingIOError,
            IncrementalNewlineDecoder,
            UnsupportedOperation,
            open_code,
            text_encoding,
        )

        assert BlockingIOError is io.BlockingIOError
        assert IncrementalNewlineDecoder is io.IncrementalNewlineDecoder
        assert UnsupportedOperation is io.UnsupportedOperation
        assert open_code is io.open_code
        assert text_encoding is io.text_encoding

    def test_custom_io_functions(self):
        """Test that custom read/write/append are importable."""
        from pyeio import append, read, write
        from pyeio.io import append as io_append
        from pyeio.io import read as io_read
        from pyeio.io import write as io_write

        assert read is io_read
        assert write is io_write
        assert append is io_append


class TestDynamicImports:
    def test_import_json(self):
        """Test that pyeio.json is lazily importable."""
        import pyeio

        json_mod = pyeio.json
        assert json_mod is not None
        assert hasattr(json_mod, "read")
        assert hasattr(json_mod, "write")
        assert hasattr(json_mod, "parse")
        assert hasattr(json_mod, "serialize")

    def test_import_toml(self):
        """Test that pyeio.toml is lazily importable."""
        import pyeio

        toml_mod = pyeio.toml
        assert toml_mod is not None
        assert hasattr(toml_mod, "read")
        assert hasattr(toml_mod, "write")
        assert hasattr(toml_mod, "parse")
        assert hasattr(toml_mod, "serialize")

    def test_import_yaml(self):
        """Test that pyeio.yaml is lazily importable."""
        import pyeio

        yaml_mod = pyeio.yaml
        assert yaml_mod is not None
        assert hasattr(yaml_mod, "read")
        assert hasattr(yaml_mod, "write")
        assert hasattr(yaml_mod, "parse")
        assert hasattr(yaml_mod, "serialize")

    def test_import_jsonl(self):
        """Test that pyeio.jsonl is lazily importable."""
        import pyeio

        jsonl_mod = pyeio.jsonl
        assert jsonl_mod is not None
        assert hasattr(jsonl_mod, "read")
        assert hasattr(jsonl_mod, "write")
        assert hasattr(jsonl_mod, "parse")
        assert hasattr(jsonl_mod, "serialize")
        assert hasattr(jsonl_mod, "append")
        assert hasattr(jsonl_mod, "extend")
        assert hasattr(jsonl_mod, "iter_parse")
        assert hasattr(jsonl_mod, "iter_read")

    def test_dynamic_import_is_cached(self):
        """Test that repeated access returns the same cached module object."""
        import pyeio

        first = pyeio.json
        second = pyeio.json
        assert first is second

    def test_dynamic_import_stored_in_globals(self):
        """Test that a dynamic import is stored in module globals after first access."""
        import pyeio

        # Ensure it's not cached yet
        pyeio.__dict__.pop("json", None)
        assert "json" not in pyeio.__dict__

        _ = pyeio.json
        assert "json" in pyeio.__dict__

    def test_unknown_attr_raises_attribute_error(self):
        """Test that accessing an unknown attribute raises AttributeError."""
        import pyeio

        with pytest.raises(AttributeError, match="nonexistent_module"):
            _ = pyeio.nonexistent_module


class TestAliases:
    def test_yml_is_yaml(self):
        """Test that pyeio.yml resolves to pyeio.yaml."""
        import pyeio

        yml_mod = pyeio.yml
        yaml_mod = pyeio.yaml
        assert yml_mod is yaml_mod

    def test_ndjson_is_jsonl(self):
        """Test that pyeio.ndjson resolves to pyeio.jsonl."""
        import pyeio

        ndjson_mod = pyeio.ndjson
        jsonl_mod = pyeio.jsonl
        assert ndjson_mod is jsonl_mod

    def test_yml_cached_in_globals(self):
        """Test that yml alias is cached after first access."""
        import pyeio

        pyeio.__dict__.pop("yml", None)
        pyeio.__dict__.pop("yaml", None)
        assert "yml" not in pyeio.__dict__

        _ = pyeio.yml
        assert "yml" in pyeio.__dict__
        assert "yaml" in pyeio.__dict__

    def test_ndjson_cached_in_globals(self):
        """Test that ndjson alias is cached after first access."""
        import pyeio

        pyeio.__dict__.pop("ndjson", None)
        pyeio.__dict__.pop("jsonl", None)
        assert "ndjson" not in pyeio.__dict__

        _ = pyeio.ndjson
        assert "ndjson" in pyeio.__dict__
        assert "jsonl" in pyeio.__dict__

    def test_yml_access_before_yaml(self):
        """Test that accessing yml first still makes yaml available."""
        import pyeio

        pyeio.__dict__.pop("yml", None)
        pyeio.__dict__.pop("yaml", None)

        yml_mod = pyeio.yml
        yaml_mod = pyeio.yaml
        assert yml_mod is yaml_mod

    def test_ndjson_access_before_jsonl(self):
        """Test that accessing ndjson first still makes jsonl available."""
        import pyeio

        pyeio.__dict__.pop("ndjson", None)
        pyeio.__dict__.pop("jsonl", None)

        ndjson_mod = pyeio.ndjson
        jsonl_mod = pyeio.jsonl
        assert ndjson_mod is jsonl_mod

    def test_yaml_access_before_yml(self):
        """Test that accessing yaml first still makes yml resolve correctly."""
        import pyeio

        pyeio.__dict__.pop("yml", None)
        pyeio.__dict__.pop("yaml", None)

        yaml_mod = pyeio.yaml
        yml_mod = pyeio.yml
        assert yaml_mod is yml_mod

    def test_jsonl_access_before_ndjson(self):
        """Test that accessing jsonl first still makes ndjson resolve correctly."""
        import pyeio

        pyeio.__dict__.pop("ndjson", None)
        pyeio.__dict__.pop("jsonl", None)

        jsonl_mod = pyeio.jsonl
        ndjson_mod = pyeio.ndjson
        assert jsonl_mod is ndjson_mod

    def test_yml_has_yaml_functions(self):
        """Test that yml alias exposes all yaml functions."""
        import pyeio

        yml_mod = pyeio.yml
        assert hasattr(yml_mod, "read")
        assert hasattr(yml_mod, "write")
        assert hasattr(yml_mod, "parse")
        assert hasattr(yml_mod, "serialize")

    def test_ndjson_has_jsonl_functions(self):
        """Test that ndjson alias exposes all jsonl functions."""
        import pyeio

        ndjson_mod = pyeio.ndjson
        assert hasattr(ndjson_mod, "read")
        assert hasattr(ndjson_mod, "write")
        assert hasattr(ndjson_mod, "parse")
        assert hasattr(ndjson_mod, "serialize")
        assert hasattr(ndjson_mod, "append")
        assert hasattr(ndjson_mod, "extend")
        assert hasattr(ndjson_mod, "iter_parse")
        assert hasattr(ndjson_mod, "iter_read")


class TestDir:
    def test_dir_contains_all_exports(self):
        """Test that dir(pyeio) contains every name in __all__."""
        import pyeio

        dir_names = dir(pyeio)
        for name in pyeio.__all__:
            assert name in dir_names, f"{name!r} missing from dir(pyeio)"

    def test_dir_matches_all(self):
        """Test that dir(pyeio) returns exactly __all__."""
        import pyeio

        assert sorted(dir(pyeio)) == sorted(pyeio.__all__)


class TestSubmoduleDirectImports:
    def test_from_pyeio_json(self):
        """Test importing pyeio.json directly."""
        import pyeio.json as json_mod

        assert hasattr(json_mod, "read")
        assert hasattr(json_mod, "parse")

    def test_from_pyeio_toml(self):
        """Test importing pyeio.toml directly."""
        import pyeio.toml as toml_mod

        assert hasattr(toml_mod, "read")
        assert hasattr(toml_mod, "parse")

    def test_from_pyeio_yaml(self):
        """Test importing pyeio.yaml directly."""
        import pyeio.yaml as yaml_mod

        assert hasattr(yaml_mod, "read")
        assert hasattr(yaml_mod, "parse")

    def test_from_pyeio_jsonl(self):
        """Test importing pyeio.jsonl directly."""
        import pyeio.jsonl as jsonl_mod

        assert hasattr(jsonl_mod, "read")
        assert hasattr(jsonl_mod, "parse")
        assert hasattr(jsonl_mod, "append")
        assert hasattr(jsonl_mod, "extend")

    def test_direct_import_matches_dynamic(self):
        """Test that direct submodule import gives the same object as dynamic access."""
        import pyeio
        import pyeio.json as json_direct
        import pyeio.jsonl as jsonl_direct
        import pyeio.toml as toml_direct
        import pyeio.yaml as yaml_direct

        assert pyeio.json is json_direct
        assert pyeio.toml is toml_direct
        assert pyeio.yaml is yaml_direct
        assert pyeio.jsonl is jsonl_direct
