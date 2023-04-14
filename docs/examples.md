---
hide:
- navigation
---

# Examples

## Save Files

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

## Save Custom Format

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

## Load Files

```json title="Input JSON File"
[1, 2, 3, 4, 5, 6]
```

```python title="Python Code"
data = easy.load("example.json")
```

```bash title="Data & Type"
[1, 2, 3, 4, 5, 6] <class 'list'>
```


## Load Custom Types

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
