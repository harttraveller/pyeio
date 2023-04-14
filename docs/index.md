---
hide:
- navigation
---

<style>
.md-typeset h1 {display: none;}
</style>

<p></p>

<div align="left">
<a href="https://github.com/harttraveller/pyeio" target="_blank">
<img src="assets/github.png" width=32 style="position: relative; left: 0px;">
</a>
<a href="https://pypi.org/project/pyeio/" target="_blank">
<img src="https://img.shields.io/pypi/v/pyeio" height=20 style="position: relative; top: -5px;">
</a>
<a href="https://github.com/harttraveller/pyeio/blob/main/LICENSE" target="_blank">
<img src="https://img.shields.io/badge/license-MIT-blue" height=20 style="position: relative; top: -5px;">
</a>
<a href="https://www.python.org/downloads" target="_blank">
<img src="https://img.shields.io/badge/python-3.10-blue" height=20 style="position: relative; top: -5px;">
</a>
<a href="https://github.com/psf/black" target="_blank">
<img src="https://img.shields.io/badge/code%20style-black-black" height=20 style="position: relative; top: -5px;">
</a>
</div>

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

## Quickstart

```bash title="Installation"
pip install pyeio
```

```python title="Usage"
from pyeio import easy
data = easy.load("data.json")
```
