# Quickstart

<div align="right">
    <a href="https://github.com/cephalon-intelligence/pyeio/blob/main/notebooks/quickstart.ipynb"  target="_blank"><img src="../assets/logo.jupyter.png" width="50" alt="jupyter" style="position: absolute; margin: -80px 0px 0px -50px;"/></a>
</div>

!!! tip "Pip Install"
    You can install the package with `pip`.

    ```bash
    pip install pyeio
    ```

!!! example "Python Import"
    The `easy` object is an instance of the `EIO` class.

    ```python
    from pyeio import easy
    ```

## Load Files

An example `JSON` file is shown below.

```json linenums="1" title="input.json"
[1, 2, 3, 4, 5, 6]
```

We can load the file with the following code.

```python linenums="1" title="load.py"
data = easy.load("input.json")
```

Printing `data` should result in the following output.

```bash linenums="1"
[1, 2, 3, 4, 5, 6] <class 'list'> # (1)!
```

1. 
    ```python title="Print Code"
    print(data, type(data))
    ```

## Load Custom Type

Using the same file from above, we can also load it as a specific type.

```python linenums="1" title="load.py"
data = easy.load("input.json", astype=np.array) # (1)!
```

1. 
   ```python title="Required Type Import"
   import numpy as np
   ```

Printing `data` will result in a different output now.


```bash linenums="1"
[1 2 3 4 5 6] <class 'numpy.ndarray'> # (1)!
```

1. 
    ```python title="Print Code"
    print(data, type(data))
    ```

## Save Files

We can also save files with the `easy` instance. 

```python linenums="1" title="save.py"
data: dict = {

}

easy.save(data, "example.json")
```

The saved file looks like this.

```json linenums="1" title="output.json"

```


## Save Custom Format


```python
from pyeio import easy
data = easy.load("example.csv", astype=dict)
print(data)
```


```python
example output
```
