## General


- Add lazily imported passthrough methods from all source
- Split the different formats into optional extras
- add cattrs, dataclasses support/overloads as an alternative to pydantic


## Formats

- csv
- txt lines where each line can have a custom parser/regexpr

## Format Specific

### JSONL

- add methods for (on file, at index):
    - insert
    - getitem
    - delitem
