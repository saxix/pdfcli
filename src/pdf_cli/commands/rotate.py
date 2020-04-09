from pathlib import Path

import click
from PyPDF4 import PdfFileReader, PdfFileWriter

from pdf_cli.commands.utils import Range
from pdf_cli.main import main


@main.command()
@click.argument('input', type=click.File('rb'))
@click.option('-p', '--pages', default=None, type=Range, help='starting page to extract')
@click.option('-o', '--output', type=click.File('wb'), required=True)
@click.option('-v', '--verbosity', type=int, default=0)
@click.option('-r', '--rotate', type=click.Choice(['left', 'right', 'inverted']), default="left")
def rotate(input, output, pages, verbosity, rotate, **kwargs):
    """rotate selected pages

Rotate selected pages and outputs in new pdf
"""
    source = PdfFileReader(input)

    angle = {'left':-90, 'right':90, 'inverted': 180}[rotate]
    if pages is None:
        pages = range(1, source.numPages)

    selection = []
    for page_num in range(1, source.getNumPages()):
        real_page = page_num - 1
        if verbosity >= 1:
            click.echo(".", nl=False)
        if verbosity >= 2:
            click.echo("Extracting page %s" % page_num)
        page = source.getPage(real_page)
        if page_num in pages:
            page._rotate(angle)
        selection.append(page)

    output_pdf = PdfFileWriter()
    for page in selection:
        output_pdf.addPage(page)

    if verbosity >= 1:
        click.echo("Writing %s" % output.name)
    output_pdf.write(output)
