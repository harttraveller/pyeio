<style>
.md-typeset h1 {display: none;}
</style>

<div align="center">
<a href="https://github.com/cephalon-intelligence/pyeio" target="_blank">
<img src="assets/pyeio-large.png" width=64 style="position: relative; left: -20px;">
</a>
<a href="https://www.python.org/downloads" target="_blank">
<img src="https://img.shields.io/badge/python-3.10-blue" height=20 style="position: relative; top: -20px;">
</a>
<a href="https://github.com/cephalon-intelligence/pyeio/blob/main/LICENSE" target="_blank">
<img src="https://img.shields.io/badge/license-MIT-blue" height=20 style="position: relative; top: -20px;">
</a>
<a href="https://github.com/cephalon-intelligence/pyeio" target="_blank">
<img src="https://img.shields.io/github/repo-size/cephalon-intelligence/pyeio" height=20 style="position: relative; top: -20px;">
</a>
<a href="https://github.com/psf/black" target="_blank">
<img src="https://img.shields.io/badge/code%20style-black-black" height=20 style="position: relative; top: -20px;">
</a>
<a href="https://docs.cephalon.io/pyeio" target="_blank">
<img src="https://img.shields.io/website?down_color=red&down_message=offline&up_color=green&up_message=online&url=https%3A%2F%2Fdocs.cephalon.io%2Fpyeio" height=20 style="position: relative; top: -20px;">
</a>
</div>
<p></p>

`Py`thon `E`asy `I`nput `O`utput: `pyeio` is a Python library meant to simplify file IO processes. The primary benefit is the ability to `load` and `save` different file types with just those methods.

=== "Before"

    ```python linenums="1"
    with open("data.json", "r") as file:
        data = json.load(file)
    file.close()
    ```

=== "After"

    ```python linenums="1"
    data = easy.load("data.json")
    ```

??? tip "Pip Install"
    You can install the package with `pip`.

    ```bash
    pip install pyeio
    ```

??? example "Python Import"
    The `easy` object is an instance of the `EIO` class.

    ```python
    from pyeio import easy
    ```

??? info "Other Features"
     Youu can also cast the loaded data to a specific type or format in the same call. I also plan on adding assorted additional functionality useful for my own development workflows.

??? abstract "Development Purpose"
    I've spent a lot of time rewriting snippets of code to load in different file formats. I find it is almost always faster to rewrite the code than find wherever you put it before. I figured I'd just centralize that functionality in one location and write some logic to handle disk IO operations on the backend.

??? question "Bug Support"
    This package is currently being actively developed - I plan on adding features when they'd facilitate other projects I'm working on. Nonetheless, feel free to submit a feature request through GitHub Issues.