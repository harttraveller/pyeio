<div align="center">
<a href="https://harttraveller.com/pyeio" target="_blank">
<img src="https://raw.githubusercontent.com/harttraveller/pyeio/main/docs/assets/pyeio-large.png" width=200>
</a>
</div>
<br>
<div align="center">

![Python](https://img.shields.io/badge/python-3.10-blue) ![GitHub](https://img.shields.io/badge/license-MIT-blue)![Code Style](https://img.shields.io/badge/code%20style-black-black)
</div>

# pyeio

Short for `Py`thon `E`asy `I`nput `O`utput, `pyeio` is a python library meant to simplify file IO processes. You can find detailed documentation by clicking the logo above.

## Details

For example, you can use it to avoid rewriting the code below hundreds of times.

```python linenums="1"
import json
with open("data/example.json", "r") as file:
    data = json.load(file)
file.close()
```

By simplifying it to the following line.

```python linenums="1"
from pyeio import EIO
easy = EIO()
data = easy.load("data/example.json")
```

While this might not seem like a large improvement, the specific benefit is twofold:

1. You can load/save *many* different file types with this one method. Furthermore, you can cast the loaded data to a specific type or format in the same call. (Under development)
2. Various additional functionality. (Under development)

## Installation


The package requires Python 3.10. I recommend configuring a Python environment on your machine and installing `pyeio` inside of it.

### User Installation

Install the current version of `pyeio` with `pip`.

```bash
pip install pyeio
```

To upgrade to a newer release use the `--upgrade` flag.

```bash
pip install pyeio --upgrade
```

### Developer Installation

First clone the repository. You can do this using SSH, or HTTPS. I recommend SSH, as it's more secure.

**SSH**

```bash
git clone git@github.com:harttraveller/pyeio.git
```

**HTTPS**

```bash
git clone https://github.com/harttraveller/pyeio.git
```

Next install the package with `pip`. The `setup.py` package contains the requirements for basic functionality, however the `requirements.txt` file also includes requirements for testing and using the notebooks.

```bash
cd pyeio
pip install -r requirements.txt
pip install -e .
```

You can update `pyeio` by running the following command in the same directory. There may be new requirements added.

```bash
git pull origin main
pip install -r requirements.txt
pip install -e . --upgrade
```

### Testing

The package uses `pytest` for testing. You can learn more about pytest on their [homepage](https://pytest.org/). To run the tests, you can run the following command.

```bash
pytest pyeio
```


