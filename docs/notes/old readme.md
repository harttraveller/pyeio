
## Details

### Format Support

Support for a given file format means that a submodule of `pyeio.file` exists, such that the following features are supported.

- Global Support:
    - `load` (from path)
    - `save` (data to path)
    - `read` (read some data, kind read depends on file format)
- List Structured Data Support:
    - `parse`
    - `apply`
    - `append`
    - `prepend`
- Tree Structured Data Support:
    - `traverse`

<!-- Experimental Features
- format identification
- ? lm based data cleaning
-->