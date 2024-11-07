# todo: this should be refactored into a extension checking engine that includes warnings
# for technically allowed file extensions, the ability to bypass checks with parameters, etc
def is_valid_file_extension(extension: str, allowed: set[str]) -> bool:
    return extension.lower() in allowed
