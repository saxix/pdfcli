# pdfcli

[![Pypi](https://badge.fury.io/py/pdfcli.svg)](https://badge.fury.io/py/pdfcli)

[//]: # ([![coverage]&#40;https://codecov.io/github/saxix/pdfcli/coverage.svg?branch=develop&#41;]&#40;https://codecov.io/github/saxix/pdfcli?branch=develop&#41;)
[![Test](https://github.com/saxix/pdfcli/actions/workflows/test.yml/badge.svg)](https://github.com/saxix/pdfcli/actions/workflows/test.yml)

[//]: # ([![Documentation]&#40;https://github.com/saxix/pdfcli/actions/workflows/docs.yml/badge.svg&#41;]&#40;https://saxix.github.io/pdfcli/&#41;)
[//]: # ([![Django]&#40;https://img.shields.io/pypi/frameworkversions/django/pdfcli&#41;]&#40;https://pypi.org/project/pdfcli/&#41;)
[//]: # ([![Supported Python versions]&#40;https://img.shields.io/pypi/pyversions/pdfcli.svg&#41;]&#40;https://pypi.org/project/pdfcli/&#41;)


pdfcli is a command line utility to work with pdf.

It is able to split,join,reorder,extract text .

    $ pdf --help
    Usage: pdf [OPTIONS] COMMAND [ARGS]...

    Options:
      --help  Show this message and exit.

    Commands:
      decrypt    decrypt pdf
      encrypt    encrypt pdf
      extract    extract one or multiple pages and build a new document.
      info       dump pdf informations.
      join       join multiple pdf together in a single file
      rotate     rotate selected pages Rotate selected pages and outputs in new...
      split      split pdf into single page file
      watermark  use first page of pdf and add it as watermark to other
                 document...
### Examples

Extract pages 1, and from 5 to 9 one file for page

    pdfcli split source.pdf -p 1,5-9

Create a new pdf using pages 1, and from 5 to 9

    pdfcli extract source.pdf  -p 1,5-9 -o new.pdf
