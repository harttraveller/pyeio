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
<p></p>

<br> 

!!! abstract "Description"
    Python Easy Input Output is a Python library meant to simplify file IO processes. The primary benefit is the ability to load and save different file formats with just those methods. I plan to add formats as they are needed for my own development purposes.


```python title="Before"
import json
with open("data.json", "r") as file:
    data = json.load(file)
file.close()
```

```python title="After"
from pyeio import easy
data = easy.load("data.json")
```


