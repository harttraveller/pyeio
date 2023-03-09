# Quickstart

## Installation

The package can be installed using pip.

```bash
pip install pyeio
```

## Import

To use the package, import `easy`.

```python
from pyeio import easy
```

## Load Files

An example `JSON` file is shown below.

```json
[1, 2, 3, 4, 5, 6]
```

We can load the file with the following code.

```python
data = easy.load("input.json")
```

Printing `data` and its type should result in the following output.

```bash
[1, 2, 3, 4, 5, 6] <class 'list'>
```

## Load Custom Type

Using the same file from above, we can also load it as a specific type.

```python
data = easy.load("input.json", astype="np.array")
```

Printing `data` will result in a different output now.


```bash
[1 2 3 4 5 6] <class 'numpy.ndarray'>
```


## Save Files

We can also save files with the `easy` instance. 

```python
data: dict = {

}

easy.save(data, "example.json")
```

The saved file looks like this.

```json

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
