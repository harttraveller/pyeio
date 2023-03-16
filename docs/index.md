---
hide:
- navigation
---

<style>
.md-typeset h1 {display: none;}
</style>


<div align="center">
<img src="assets/pyeio-large.png" width=64 style="position: relative; left: -8px;">
<a href="https://github.com/harttraveller/pyeio" target="_blank">
<img src="assets/github.png" width=32 style="position: relative; left: -4px; top: -15px;">
</a>
<a href="https://github.com/harttraveller/pyeio/blob/main/LICENSE" target="_blank">
<img src="https://img.shields.io/badge/license-MIT-blue" height=20 style="position: relative; top: -20px;">
</a>
<a href="https://www.python.org/downloads" target="_blank">
<img src="https://img.shields.io/badge/python-3.10-blue" height=20 style="position: relative; top: -20px;">
</a>
<a href="https://github.com/psf/black" target="_blank">
<img src="https://img.shields.io/badge/code%20style-black-black" height=20 style="position: relative; top: -20px;">
</a>
</div>

<br>

??? warning "Status: Preliminary Development"
    I plan on addding formats as they are needed for relevant development purposes.

## Overview

Python Easy Input Output is a Python library meant to simplify file IO processes. The primary benefit is the ability to load and save different file formats with just the `load` and `save` methods.

=== "Before"
    ```python
    import json
    with open("data.json", "r") as file:
        data = json.load(file)
    file.close()
    ```

=== "After"
    ```python
    from pyeio import easy
    data = easy.load("data.json")
    ```

```bash title="Installation"
pip install pyeio
```

```python title="Import"
from pyeio import easy
```

## Tutorial

### Save Files

```python title="Input Dictionary"
data = {
    "apples": 3,
    "oranges": 4,
    "bananas": 5
}
```

```python title="Python Code"
easy.save(data, "example.json")
```

```json title="Output JSON File"
{
    "apples": 3,
    "oranges": 4,
    "bananas": 5
}
```

### Save Custom Format

```python title="Input Dictionary"
data = {
    "apples": 3,
    "oranges": 4,
    "bananas": 5
}
```

```python title="Python Code"
easy.save(data, "example.csv")
```

```python title="Output CSV File"
apples, 3
oranges, 4
bananas, 5
```

### Load Files

```json title="Input JSON File"
[1, 2, 3, 4, 5, 6]
```

```python title="Python Code"
data = easy.load("example.json")
```

```bash title="Data & Type"
[1, 2, 3, 4, 5, 6] <class 'list'>
```


### Load Custom Types

```python title="Additional Import"
from pyeio import kind
```

```json title="Input JSON File"
[1, 2, 3, 4, 5, 6]
```

```python title="Python Code"
data = easy.load("example.json", astype=kind.numpy.array)
```

```bash title="Data & Type"
[1 2 3 4 5 6] <class 'numpy.ndarray'>
```

## File Formats
### Implemented
- json

### Priority
- jsonl


### Backlog
- csv
- xlsx
- txt
- pickle
- hdf5
- db
- sqlite
- html
- zip
- gz
- pdf
- docx
- png
- jpg
- jpeg
- mat
- npy
- npz
- 7z
- graphml
- js
- py
- null (no extension, assumed binary or text)
- bin
- toml
- yaml
- zst
- sql
- sqlitedict