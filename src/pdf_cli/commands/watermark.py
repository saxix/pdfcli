import sys
from io import BytesIO, StringIO
from pathlib import Path

import click
from PyPDF4 import PdfFileReader, PdfFileWriter

from pdf_cli.commands.utils import Range
from pdf_cli.main import main


@main.command()
@click.argument('input', type=click.File('rb'))
@click.argument('watermark', type=click.File('rb'))
@click.option('-o', '--output', type=click.File('wb'), required=True)
@click.option('-v', '--verbosity', type=int, default=0)
def watermark(input, watermark, output, verbosity, **kwargs):
    """use first page of pdf and add it as watermark to other document

es. pdfcli watermark wm.pdf source.pdf -o final.pdf

"""
    watermark = PdfFileReader(watermark)
    watermarkpage = watermark.getPage(0)

    pdf = PdfFileReader(input)
    pdfwrite = PdfFileWriter()
    for page in range(pdf.getNumPages()):
        pdfpage = pdf.getPage(page)
        pdfpage.mergePage(watermarkpage)
        pdfwrite.addPage(pdfpage)

    pdfwrite.write(output)
