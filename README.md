# Page Loader

[![Actions Status](https://github.com/justpwned/python-project-lvl3/actions/workflows/ci.yml/badge.svg)](https://github.com/justpwned/python-project-lvl3/actions/workflows/ci.yml)
[![Maintainability](https://api.codeclimate.com/v1/badges/0432c15d9d2169c4f683/maintainability)](https://codeclimate.com/github/justpwned/python-project-lvl3/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/0432c15d9d2169c4f683/test_coverage)](https://codeclimate.com/github/justpwned/python-project-lvl3/test_coverage)

Page Loader is a command line tool and library for downloading web pages.

## How it works

Page Loader sends GET HTTP request to the user specified resource. If a requested web page happens to be an HTML
document it will also download any required assets contained in
```img``` ```script``` ```link``` ```audio``` ```video``` ```source``` ```object``` ```track``` tags and replaces their
source attributes to valid file paths with the extension being determined based on the mimetype. If downloading an asset
results in an HTTP error, the program will ignore it and proceed with downloading remaining assets.
*Unfortunately though*, due to the way that a lot of modern websites are built (lots of dynamically generated content,
styles, etc.)
it's not always possible to download a page preserving its original design

### Built with

- [Requests](https://docs.python-requests.org/en/master/)
- [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [Progress](https://github.com/verigak/progress)
- [Pytest](https://docs.pytest.org/en/6.2.x/)
- [Requests-mock](https://github.com/jamielennox/requests-mock)

This project also uses [Github Actions](https://github.com/features/actions) as a CI utility to automatically run tests
and linter on each commit to repository

## Getting Started

### Prerequisites

- [Poetry](https://python-poetry.org/)

### Installation

1. Clone repository

```bash
git clone https://github.com/justpwned/page-loader.git
```

2. Install all the dependencies, build the package and install it

```
make package-install
```

## Usage

### Library example

```python
import page_loader

try:
    url = 'https://stackoverflow.com/questions/1319615/proper-way-to-declare-custom-exceptions-in-modern-python'
    out_filepath = page_loader.download(url)
    print(out_filepath)
except page_loader.exceptions.PageLoaderException as ex:
    print(ex)
```

### CLI example

```
usage: page-loader [-h] [-o OUTPUT] url

Download a web page

positional arguments:
  url                   URL of the page to download

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Output directory (default: current directory)
```

## Demo
![Demo](demo.gif)