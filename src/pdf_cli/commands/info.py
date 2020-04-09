from pathlib import Path

import click
from PyPDF4 import PdfFileReader, PdfFileWriter

from pdf_cli.main import main

@main.command()
@click.argument('input', type=click.File('rb'))
@click.option('-v', '--verbosity', type=int, default=0)
def info(input, verbosity, **kwargs):
    """dump pdf informations.

pdfcli info source.pdf

"""

    pdf = PdfFileReader(input)
    information = pdf.getDocumentInfo()
    number_of_pages = pdf.getNumPages()

    txt = f"""
 Filename: {input.name}
 Author: {information.author}
 Creator: {information.creator}
 Producer: {information.producer}
 Subject: {information.subject}
 Title: {information.title}
 Number of pages: {number_of_pages}"""
    print(txt)
