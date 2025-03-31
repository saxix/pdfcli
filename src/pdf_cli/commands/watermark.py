from typing import Any

import click
from pypdf import PdfReader, PdfWriter

from pdf_cli.main import main


@main.command()
@click.argument("input_file", type=click.File("rb"))
@click.argument("watermark", type=click.File("rb"))
@click.option("-o", "--output", type=click.File("wb"), required=True)
@click.option("-v", "--verbosity", type=int, default=0)
def watermark(input_file: click.File, watermark: click.File, output: click.File, **kwargs: Any) -> None:  # noqa: ARG001
    """use first page of pdf and add it as watermark to other document"""
    wm = PdfReader(watermark)  # type: ignore[arg-type]
    watermark_page = wm.pages[0]

    pdf = PdfReader(input_file)  # type: ignore[arg-type]
    pdfwrite = PdfWriter()
    for page in range(len(pdf.pages)):
        pdfpage = pdf.pages[page]
        pdfpage.merge_page(watermark_page)
        pdfwrite.add_page(pdfpage)

    pdfwrite.write(output)  # type: ignore[arg-type]
