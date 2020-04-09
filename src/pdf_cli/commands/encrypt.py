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
def encrypt(input, output, password, verbosity, **kwargs):
    """encrypt pdf.

pdfcli encrypt source.pdf -o crypted.pdf -p password

"""

    source = PdfFileReader(input)
    output_pdf = PdfFileWriter()
    for page in source.pages:
        output_pdf.addPage(page)

    output_pdf.encrypt(user_pwd=password)

    if verbosity >= 1:
        click.echo("Writing %s" % output.name)
    output_pdf.write(output)
