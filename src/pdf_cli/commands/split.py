from pathlib import Path

import click
from PyPDF4 import PdfFileReader, PdfFileWriter

from pdf_cli.commands.utils import Range
from pdf_cli.main import main


@main.command()
@click.option('-p', '--pages', default=None, type=Range, help='starting page to extract')
@click.option('--format', default="page-%02d.pdf", help='page filename pattern')
@click.argument('input', type=click.File('rb'))
@click.option('-d', '--destination', type=click.Path(exists=False), default='.')
@click.option('-v', '--verbosity', type=int, default=0)
def split(input, destination, pages, format, verbosity, **kwargs):
    """split pdf into single page file.

pdfcli split document.pdf --format page-%02d.pd -p 1,10-20

"""
    source = PdfFileReader(input)
    if pages is None:
        pages = range(1, source.numPages+1)

    to_dir = Path(destination)
    if not to_dir.exists():
        to_dir.mkdir(parents=True)

    for page_num in pages:
        real_page = page_num - 1
        if verbosity >= 1:
            click.echo("Extracting page %s" % page_num)
        # due to a bug PyPDF4 file need to be reopened
        source = PdfFileReader(input)
        dest_file = (to_dir / Path(format % page_num)).absolute()
        page = source.getPage(real_page)
        output_pdf = PdfFileWriter()
        output_pdf.addPage(page)
        with open(str(dest_file), "wb") as f:
            output_pdf.write(f)
