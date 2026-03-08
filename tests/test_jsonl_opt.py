import builtins as _builtins
from pathlib import Path

import orjson
import pytest

from pyeio.jsonl._jsonl import (
    _BufferedLineReader,
    iter_read,
)


class _ReadTracker:
    """Wraps a binary file object to count ``read()`` calls and bytes consumed."""

    __slots__ = ("_fh", "bytes_read", "read_count")

    def __init__(self, fh):
        self._fh = fh
        self.bytes_read: int = 0
        self.read_count: int = 0

    def read(self, size: int = -1):
        data = self._fh.read(size)
        self.bytes_read += len(data)
        self.read_count += 1
        return data

    def close(self):
        self._fh.close()

    @property
    def closed(self) -> bool:
        return self._fh.closed


@pytest.fixture
def _patch_open(monkeypatch):
    """
    Monkeypatches ``builtins.open`` inside the jsonl module and returns a list
    that collects every ``_ReadTracker`` wrapper created during the test.
    """
    import pyeio.jsonl._jsonl as _mod

    trackers: list[_ReadTracker] = []
    _real_open = _builtins.open

    def _tracking_open(*args, **kwargs):
        fh = _real_open(*args, **kwargs)
        tracker = _ReadTracker(fh)
        trackers.append(tracker)
        return tracker

    monkeypatch.setattr(_mod.builtins, "open", _tracking_open)
    return trackers


@pytest.fixture
def large_jsonl_file(tmp_path: Path) -> Path:
    """Creates a ~12 MB JSONL file with 100 000 lines (~120 bytes each)."""
    file = tmp_path / "large.jsonl"
    lines = [orjson.dumps({"index": i, "data": "x" * 80}) for i in range(100_000)]
    file.write_bytes(b"\n".join(lines) + b"\n")
    return file


class TestBufferedLineReader:
    def test_reads_all_lines(self, tmp_path: Path):
        """Test that every non-empty line in the file is yielded."""
        file = tmp_path / "test.jsonl"
        file.write_bytes(b'{"a":1}\n{"b":2}\n{"c":3}\n')
        with _BufferedLineReader(file) as reader:
            lines = list(reader)
        assert len(lines) == 3
        assert orjson.loads(lines[0]) == {"a": 1}
        assert orjson.loads(lines[2]) == {"c": 3}

    def test_skips_empty_lines(self, tmp_path: Path):
        """Test that blank lines are silently skipped."""
        file = tmp_path / "test.jsonl"
        file.write_bytes(b'{"a":1}\n\n\n{"b":2}\n\n')
        with _BufferedLineReader(file) as reader:
            lines = list(reader)
        assert len(lines) == 2

    def test_strips_whitespace(self, tmp_path: Path):
        """Test that leading/trailing whitespace on lines is stripped."""
        file = tmp_path / "test.jsonl"
        file.write_bytes(b'  {"a":1}  \n  {"b":2}  \n')
        with _BufferedLineReader(file) as reader:
            lines = list(reader)
        assert lines == [b'{"a":1}', b'{"b":2}']

    def test_empty_file(self, tmp_path: Path):
        """Test that an empty file yields nothing."""
        file = tmp_path / "empty.jsonl"
        file.write_bytes(b"")
        with _BufferedLineReader(file) as reader:
            lines = list(reader)
        assert lines == []

    def test_single_line_no_trailing_newline(self, tmp_path: Path):
        """Test that a file with no trailing newline still yields the last line."""
        file = tmp_path / "test.jsonl"
        file.write_bytes(b'{"a":1}')
        with _BufferedLineReader(file) as reader:
            lines = list(reader)
        assert lines == [b'{"a":1}']

    def test_context_manager_closes_handle(self, tmp_path: Path):
        """Test that exiting the context manager closes the file handle."""
        file = tmp_path / "test.jsonl"
        file.write_bytes(b'{"a":1}\n')
        with _BufferedLineReader(file) as reader:
            pass
        assert reader._fh.closed

    def test_close_closes_handle(self, tmp_path: Path):
        """Test that calling close() closes the underlying file handle."""
        file = tmp_path / "test.jsonl"
        file.write_bytes(b'{"a":1}\n')
        reader = _BufferedLineReader(file)
        assert not reader._fh.closed
        reader.close()
        assert reader._fh.closed

    def test_is_own_iterator(self, tmp_path: Path):
        """Test that __iter__ returns self."""
        file = tmp_path / "test.jsonl"
        file.write_bytes(b'{"a":1}\n')
        reader = _BufferedLineReader(file)
        assert iter(reader) is reader
        reader.close()


class TestBufferedLineReaderChunking:
    def test_block_size_smaller_than_line(self, tmp_path: Path):
        """Test correctness when a single line spans multiple read chunks."""
        file = tmp_path / "test.jsonl"
        # Each line is ~20 bytes; block_size=8 forces multiple reads per line.
        file.write_bytes(b'{"key":"value_aaa"}\n{"key":"value_bbb"}\n')
        with _BufferedLineReader(file, size=8) as reader:
            lines = list(reader)
        assert len(lines) == 2
        assert orjson.loads(lines[0]) == {"key": "value_aaa"}
        assert orjson.loads(lines[1]) == {"key": "value_bbb"}

    def test_block_size_one_byte(self, tmp_path: Path):
        """Extreme edge case: one byte per read still produces correct output."""
        file = tmp_path / "test.jsonl"
        file.write_bytes(b'{"a":1}\n{"b":2}\n')
        with _BufferedLineReader(file, size=1) as reader:
            lines = list(reader)
        assert len(lines) == 2
        assert orjson.loads(lines[0]) == {"a": 1}
        assert orjson.loads(lines[1]) == {"b": 2}

    def test_block_size_larger_than_file(self, tmp_path: Path):
        """Test that a block_size larger than the file works in a single read."""
        file = tmp_path / "test.jsonl"
        file.write_bytes(b'{"a":1}\n{"b":2}\n')
        with _BufferedLineReader(file, size=1 << 20) as reader:
            lines = list(reader)
        assert len(lines) == 2

    def test_line_exactly_at_block_boundary(self, tmp_path: Path):
        """Test a line whose newline falls exactly at a chunk boundary."""
        # "ABCDE\n" is 6 bytes; with block_size=6 the newline is the last
        # byte of the first chunk.
        line_a = b'{"x":1}'  # 7 bytes
        line_b = b'{"y":2}'
        payload = line_a + b"\n" + line_b + b"\n"
        block_size = len(line_a) + 1  # newline is last byte of first chunk

        file = tmp_path / "test.jsonl"
        file.write_bytes(payload)
        with _BufferedLineReader(file, size=block_size) as reader:
            lines = list(reader)
        assert len(lines) == 2
        assert lines[0] == line_a
        assert lines[1] == line_b

    def test_many_lines_various_block_sizes(self, tmp_path: Path):
        """Parameterised sanity check across several block sizes."""
        file = tmp_path / "test.jsonl"
        expected = [{"i": i} for i in range(50)]
        file.write_bytes(b"\n".join(orjson.dumps(obj) for obj in expected) + b"\n")
        for block_size in (1, 7, 13, 64, 256, 4096):
            with _BufferedLineReader(file, size=block_size) as reader:
                parsed = [orjson.loads(line) for line in reader]
            assert parsed == expected, f"Failed with block_size={block_size}"

    def test_crlf_line_endings(self, tmp_path: Path):
        """Test that CRLF line endings are handled correctly."""
        file = tmp_path / "test.jsonl"
        file.write_bytes(b'{"a":1}\r\n{"b":2}\r\n')
        with _BufferedLineReader(file, size=10) as reader:
            lines = list(reader)
        assert len(lines) == 2
        assert orjson.loads(lines[0]) == {"a": 1}
        assert orjson.loads(lines[1]) == {"b": 2}


class TestStreamingProfiling:
    """
    Tests that verify the streaming reader only performs the minimum I/O
    necessary and properly manages file handles.
    """

    def test_partial_iteration_reads_minimal_bytes(self, large_jsonl_file: Path):
        """Reading 5 lines from a large file should consume << 1 % of it."""
        total_size = large_jsonl_file.stat().st_size
        block_size = 1 << 16  # 64 KiB

        reader = _BufferedLineReader(large_jsonl_file, size=block_size)
        try:
            count = 0
            for _ in reader:
                count += 1
                if count >= 5:
                    break
            bytes_consumed = reader._fh.tell()
        finally:
            reader.close()

        assert count == 5
        # At most a couple of chunks should have been read.
        assert bytes_consumed <= block_size * 2
        assert bytes_consumed < total_size * 0.01

    def test_full_iteration_consumes_entire_file(self, large_jsonl_file: Path):
        """Exhausting the reader should consume the entire file."""
        total_size = large_jsonl_file.stat().st_size

        reader = _BufferedLineReader(large_jsonl_file)
        try:
            count = sum(1 for _ in reader)
            bytes_consumed = reader._fh.tell()
        finally:
            reader.close()

        assert count == 100_000
        assert bytes_consumed == total_size

    def test_iter_read_n_reads_minimal_bytes(
        self, large_jsonl_file: Path, _patch_open: list[_ReadTracker]
    ):
        """``iter_read`` with ``n=5`` should read a tiny fraction of the file."""
        block_size = 1 << 16

        result = list(iter_read(large_jsonl_file, n=5, block_size=block_size))
        assert len(result) == 5

        assert len(_patch_open) == 1
        tracker = _patch_open[0]
        assert tracker.bytes_read <= block_size * 2
