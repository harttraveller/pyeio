# Ontology

Any given data format has certain structural properties. Many data formats share these structural properties, allowing them to be grouped into categories. A broader 'ontology of data formats' is a side effect of building this library.

## Hierarchy

- binary
    - text (json, py)
    - text_special_embedded (pdf)
    - special (jpeg, xlsx)

- table
- image
    - image/frame sequence (gif, mp4)

## Properties

### Root Level Array vs. Tree

For example, JSON files have an inherent key-value 'tree-like' structure of arbitrary depth and type. Accordingly, it is very difficult to only read in and successfully parse part of a JSON file. EG: Parsing just the first name out of the JSON file below would be complicated. This 'tree-like' structural property is shared with YAML, TOML, etc.

```json
{
    "name": {
        "first": "John",
        "last": "Smith"
    },
    "job_title": "Engineer",
}
```

Whereas JSONL (newline delimited JSON) has an inherent 'array-like' structure, at the 'first level' at least. Each element in that first level array has a 'tree-like' structure.

```json
{"name":{"first":"John","last": "Smith"},"job_title": "Engineer"}
{"name":{"first":"Sally","last":"Perkins"},"job_title":"Scientist"}
```

The key point being that while it makes sense to be able to read in lines of array-like data (eg: JSONL) line by line, it doesn't make sense to do this with tree-like data (eg: JSON). The method associated with each of the formats are