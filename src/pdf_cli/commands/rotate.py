from pathlib import Path
from typing import Any

import click
from pypdf import PageObject, PdfReader, PdfWriter

from pdf_cli.commands.utils import Range
from pdf_cli.main import main

ANGLES = {"left": -90, "right": 90, "inverted": 180}


@main.command()
@click.argument("input_file", type=click.File("rb"))
@click.option("-p", "--pages", default=None, type=Range, help="starting page to extract")
@click.option("-o", "--output", type=click.File("wb"), required=False)
@click.option("-v", "--verbosity", type=int, default=0)
@click.option("-r", "--rotate", type=click.Choice(["left", "right", "inverted"]), default="left")
def rotate(
    input_file: click.File,
    output: click.File,
    pages: list[int],
    verbosity: int,
    rotate: str,
    **kwargs: Any,  # noqa: ARG001
) -> None:
    """Rotate selected pages and outputs in new pdf"""
    source = PdfReader(input_file)  # type: ignore[arg-type]

    angle = ANGLES.get(rotate) or 0
    if pages is None:
        pages = Range(f"1-{len(source.pages)}", "")
    if output is None:
        output = Path(input_file.name).with_suffix(".rotated.pdf")
    selection = []
    for page_num in pages:
        real_page = page_num - 1
        if verbosity >= 2:
            click.echo(f"Rotating page {page_num}")
        elif verbosity >= 1:
            click.echo(".", nl=False)
        page: PageObject = source.pages[real_page]
        page.rotation = angle
        selection.append(page)

    output_pdf = PdfWriter()
    for page in selection:
        output_pdf.add_page(page)

    if verbosity >= 1:
        click.echo(f"Writing {output.name}")
    output_pdf.write(output)  # type: ignore[arg-type]
