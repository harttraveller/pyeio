# Todo

## Requirements

## Stretch Goals

- Reduce external dependencies to > n (some low number) for all file formats
- Benchmark and try to speed up all operations.
- Use Result

## Features

### Dependencies




### Security

- pdfid - security analysis and deactivation of potentially malicious pdfs
- detection of whether archive is zip bomb
- google safebrowsing integration for downloading files, urls
- scrub/randomize exif metadata from images
- scrub/randomize generic metadata in files
- add some encryption utilities

### Analysis

### Unsorted

- check file integrity (hashes)
- check data integrity (parsable according to spec)
- fix data integrity (attempt to identify problem in corrupted data and fix it)
- get file size (raw and when in archive)
    - rough estimation for large files, return est. range?
    - compute with certainty (much slower)
- get in memory data size (pympler)
- estimate number of text lines in file
    - rough estimation for large files, return est. range?
    - compute with certainty (much slower)
        - implement on disk cache of file/data hash so computation is accelerated for same file?
- estimate unpacked file size
- get file metadata (exif data, on disk metadata, pdf metadata)
- search disk for file
- use magic, chardet, langdetect(?) for identification of data/file properties/types
- (generic util) look at file/data entropy
- when downloading files, implement on disk caching for data based on hashes to avoid duplicative downloads?
    - would need to allow bypass
- pydantic schema generation and validation
- automated data cleaning
- when there isn't any file extension, and the automatic loaders are used, the system should try and use python-magic to identify the file format
- add feature to write msgspec/pydantic models from data
- add feature to dynamically generate in memory pydantic models for validation
    - jsonschema validation?
- do file format analysis using stack exchange sites/stack overflow data
- gather file metadata
- move files
- rename files
- grep in files/across files
- search files system
- get metadata about file system
- estimate/calc files/data size
- estimate/calc num lines
- estimate/calc num blocks
- estimate/calc num chars


### Maybe?

- optional integration of web module with proxy service?
- fake user agent generation
- web crawling/evaluation with llm?
- create hierarchy of format sets - svg can be loaded by xml parser, md by txt, but pdf not by json, etc