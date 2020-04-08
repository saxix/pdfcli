from pathlib import Path

import click
from PyPDF4 import PdfFileReader, PdfFileWriter

from pdf_cli.commands.utils import Range
from pdf_cli.main import main


@main.command()
@click.option('-p', '--pages', default=None, type=Range, help='starting page to extract')
@click.argument('input', type=click.File('rb'))
@click.option('-o', '--output', type=click.File('wb'), required=True)
@click.option('-v', '--verbosity', type=int, default=0)
def extract(input, output, pages, verbosity, **kwargs):
    """extract one or multiple pages and build a new document."""
    source = PdfFileReader(input)

    if pages is None:
        pages = range(1, source.numPages)

    selection = []
    for page_num in pages:
        real_page = page_num - 1
        if verbosity >= 1:
            click.echo(".", nl=False)
        if verbosity >= 2:
            click.echo("Extracting page %s" % page_num)
        # due to a bug PyPDF4 file need to be reopened
        selection.append(source.getPage(real_page))

    output_pdf = PdfFileWriter()
    for page in selection:
        output_pdf.addPage(page)

    if verbosity >= 1:
        click.echo("Writing %s" % output.name)
    output_pdf.write(output)
