# pyeio

<div align="left">
<a href="https://harttraveller.com/pyeio" target="_blank">
<img src="https://raw.githubusercontent.com/harttraveller/pyeio/main/docs/assets/pyeio-large.png" height=20>
</a>
<a href="https://pypi.org/project/pyeio/" target="_blank">
<img src="https://img.shields.io/pypi/v/pyeio" height=20>
</a>
<a href="https://github.com/harttraveller/pyeio/blob/main/LICENSE" target="_blank">
<img src="https://img.shields.io/badge/license-MIT-blue" height=20>
</a>
<a href="https://www.python.org/downloads" target="_blank">
<img src="https://img.shields.io/badge/python-3.10-blue" height=20>
</a>
<a href="https://github.com/psf/black" target="_blank">
<img src="https://img.shields.io/badge/code%20style-black-black" height=20>
</a>
</div>

<br>

Short for `Py`thon `E`asy `I`nput `O`utput, `pyeio` is a python library meant to simplify file IO processes.

```bash
pip install pyeio
```

For example, you can use it to avoid rewriting the code below hundreds of times.

```python
import json
with open("data/example.json", "r") as file:
    data = json.load(file)
file.close()
```

By simplifying it to the following line.

```python
from pyeio import easy
data = easy.load("data.json")
```

For more examples visit the [documentation](https://harttraveller.com/pyeio) site.




