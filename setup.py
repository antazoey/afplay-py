#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import find_packages, setup

extras_require = {
    "test": ["pytest>=7.0", "pytest-mock>=3.10.0,<4"],
    "lint": [
        "black>=23.3.0",
        "mypy>=1.0,<2",
        "types-requests",
        "types-setuptools",
        "flake8>=5.0.4",
        "isort>=5.10.1",
        "mdformat>=0.7.16",
        "mdformat-gfm>=0.3.5",
        "mdformat-frontmatter>=0.4.1",
    ],
    "doc": [
        "Sphinx>=3.4.3,<4",
        "sphinx_rtd_theme>=0.1.9,<1",
        "towncrier>=19.2.0, <20",
    ],
    "release": [
        "setuptools",
        "setuptools-scm",
        "wheel",
        "twine==3.8",
    ],
    "vlc": [
        "python-vlc>=3.0.18121,<4",
    ],
}

# NOTE: `pip install -e .[dev]` to install package
extras_require["dev"] = (
    extras_require["test"]
    + extras_require["lint"]
    + extras_require["doc"]
    + extras_require["release"]
    + extras_require["vlc"]
)

with open("./README.md") as readme:
    long_description = readme.read()


setup(
    name="afplay-py",
    use_scm_version=True,
    setup_requires=["setuptools_scm"],
    description="A wrapper around macOS afplay",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Juliya Smith <juliya@juliyasmith.com>",
    author_email="juliya@juliyasmith.com",
    url="https://github.com/unparalleled-js/afplay-py",
    include_package_data=True,
    install_requires=[],
    python_requires=">=3.9,<4",
    extras_require=extras_require,
    py_modules=["afplay"],
    license="Apache-2.0",
    zip_safe=False,
    keywords="afplay,macos",
    packages=find_packages(exclude=["tests", "tests.*"]),
    package_data={"afplay": ["py.typed"]},
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: MacOS",
        "Operating System :: POSIX",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)
