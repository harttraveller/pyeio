## General

- Add lazily imported passthrough methods from all source
- Split the different formats into optional extra dependencies
- add cattrs, dataclasses support/overloads as an alternative to pydantic

## Formats

### Unsorted

- ini
- cbor2
- parquet
- npz
- the data format the sunkcosts used that I forget the name of
- uml
- graphml
- markdown (with parser?)

### Text Data


#### Key value

- dotenv / env

#### Row based with header

- csv

#### Line based

- txt lines where each line can have a custom parser/regexpr
    - can be adapted for stuff like log files

#### Structured object

- xml
- json5

### Image

- png
- jpg/jpeg

### Archives

Note that archives can have multiple different data types, so it may be useful to implement a pattern that either:

1. chains an archive format to a specific other normal format
2. or allows passing in a sub/normal format handler either as a callable or a literal string as a parameter

- zstandard
- zip
- tar.gz
- 7zip

## Format Specific

### JSONL

- add methods for (on file, at index):
    - insert
    - getitem
    - delitem
    - filter (search, where matching predicate)
    - map
