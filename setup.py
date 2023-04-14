from pathlib import Path
from setuptools import setup, find_packages

setup(
    name="pyeio",
    description="Python library for easy input/output file operations.",
    version="0.0.5",
    license="MIT",
    author="Hart Traveller",
    url="https://github.com/harttraveller/pyeio",
    long_description=(Path(__file__).parent / "README.md").read_text(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    include_package_data=True,
    install_requires=["pathlib", "orjson", "toml"],
)
