from pathlib import Path

import click
from PyPDF4 import PdfFileReader, PdfFileWriter

from pdf_cli.commands.utils import Range
from pdf_cli.main import main


@main.command()
@click.argument('input', type=click.File('rb'))
@click.option('-o', '--output', type=click.File('wb'), required=True)
@click.option('-v', '--verbosity', type=int, default=0)
@click.option('-p', '--password', type=str)
def decrypt(input, output, password, verbosity, **kwargs):
    """decrypt pdf.

pdfcli decrypt crypted.pdf -o clear.pdf -p password

"""
    source = PdfFileReader(input)
    source.decrypt(password)
    output_pdf = PdfFileWriter()
    for page in source.pages:
        output_pdf.addPage(page)
    if verbosity >= 1:
        click.echo("Writing %s" % output.name)
    output_pdf.write(output)
