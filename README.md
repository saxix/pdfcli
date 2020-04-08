# pdfcli

pdfcli is a command line utility to work with pdf.

It is able to split,join,reorder,extract pdf.

    Usage: pdfcli [OPTIONS] COMMAND [ARGS]...
    
    Options:
      --help  Show this message and exit.
    
    Commands:
      extract  extract one or multiple pages and build a new document.
      info     dump pdf informations.
      join     join multiple pdf together in a single file
      split    split pdf into single page file

### Examples

Extract pages 1, and from 5 to 9 one file for page

    pdfcli split source.pdf -p 1,5-9
    
Create a new pdf using pages 1, and from 5 to 9 

    pdfcli extract source.pdf  -p 1,5-9 -o new.pdf
