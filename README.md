# pdf-cli

[![Pypi](https://badge.fury.io/py/pdfcli.svg)](https://badge.fury.io/py/pdfcli)
[![Test](https://github.com/saxix/pdfcli/actions/workflows/test.yml/badge.svg)](https://github.com/saxix/pdfcli/actions/workflows/test.yml)
[![coverage](https://codecov.io/github/saxix/pdfcli/coverage.svg?branch=develop)](https://codecov.io/github/saxix/pdfcli?branch=develop)
[![Documentation](https://github.com/saxix/pdfcli/actions/workflows/docs.yml/badge.svg)](https://saxix.github.io/pdfcli/)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/pdf-cli.svg)](https://pypi.org/project/pdf-cli/)


pdfcli is a command line utility to work with pdf.

It is able to split,join,reorder,extract text .

    $ pdf --help
    Usage: pdf [OPTIONS] COMMAND [ARGS]...

    Options:
      --version
      --help     Show this message and exit.

    Commands:
      decrypt    Remove password protection from PDF files.
      encrypt    Add password protection to PDF files.
      extract    extract one or multiple pages and build a new document.
      info       dump pdf information.
      join       join multiple pdf together in a single file.
      ocr        Extract text from PDF using OCR (requires tesseract)
      rotate     Rotate selected pages and outputs in new pdf
      split      split pdf into multiple single page file.
      watermark  use first page of pdf and add it as watermark to other document


### Examples

Extract pages 1, and from 5 to 9 one file for page

    pdf split source.pdf -p 1,5-9

Create a new pdf using pages 1, and from 5 to 9

    pdf extract source.pdf  -p 1,5-9 -o new.pdf
