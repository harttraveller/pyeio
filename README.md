# pyeio

<br>
<div align="left">
<a href="https://harttraveller.github.io/pyeio" target="_blank">
<img src="https://raw.githubusercontent.com/harttraveller/pyeio/main/docs/assets/pyeio-large.png" height=20>
</a>
<a href="https://pypi.org/project/pyeio/" target="_blank">
<img src="https://img.shields.io/pypi/v/pyeio" height=20>
</a>
<a href="https://github.com/harttraveller/pyeio/blob/main/LICENSE" target="_blank">
<img src="https://img.shields.io/badge/license-MIT-blue" height=20>
</a>
</div>

<br>

Short for `Py`thon `E`asy `I`nput `O`utput, `pyeio` is a python library meant to simplify file IO processes.

## Installation

```bash
pip install pyeio
```

## Details

### Format Support

Support for a given file format means that a submodule of `pyeio.file` exists, such that the following features are supported.

- Global Support:
    - `load`
    - `save`
    - `read` (read some data, kind read depends on file format)
- List Structured Data Support:
    - `parse`
    - `apply`
- Tree Structured Data Support:
    - `traverse`

<!-- Experimental Features
- format identification
- ? lm based data cleaning
-->

#### File Loading

```python
from pyeio import file

data = file.json.load("/path/to/file")
```


#### Object Streaming

For file formats that consist of arrays of objects.

```python
from pyeio import file

for line in file.jsonl.stream("/path/to/file"):
    some_operation_on_line(line)
```



### File Formats



<!-- ## Capabilities

This package only deals with data formats that can be loaded into native python data structures, pandas dataframes, and arrays/matrices that can be handled by numpy. To minimize dependencies and scope creep, it:

1. Doesn't deal with data formats that require a continual connection to the data source (eg: sqlite databases).
2. Doesn't include syntax parsers for executable/interpreted languages (eg: python, javascript). This means that while you can load python or javascript, these are treated as plain text. If you want to navigate the AST, this should be handled separately.
3. Doesn't include packages for handling complex data formats. For example, you can load a PDF as a binary file, or even as the raw text defining the files internal schema (you almost certainly don't want to do this), but PDF parsers like pdfplumber/pdfminer aren't included, because if they were included for PDF then to be consistent dependencies and support for a [ton of other formats](https://www.wikiwand.com/en/articles/List_of_file_formats) would also have to be included, which is totally out of scope. -->
