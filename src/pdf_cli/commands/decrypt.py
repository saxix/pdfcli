from typing import Any

import click
from pypdf import PdfReader, PdfWriter

from pdf_cli.main import main


@main.command()
@click.argument("input_file", type=click.File("rb"))
@click.option("-o", "--output", type=click.File("wb"), required=True)
@click.option("-v", "--verbosity", type=int, default=0)
@click.option("-p", "--password", type=str)
def decrypt(input_file: click.File, output: click.File, password: str, verbosity: int, **kwargs: Any) -> None:  # noqa: ARG001
    """Remove password protection from PDF files."""
    source = PdfReader(input_file)  # type: ignore[arg-type]
    source.decrypt(password)
    output_pdf = PdfWriter()
    for page in source.pages:
        output_pdf.add_page(page)
    if verbosity >= 1:
        click.echo(f"Writing {output.name}")
    output_pdf.write(output)  # type: ignore[arg-type]
