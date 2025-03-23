import io
from pathlib import Path
from typing import Any

import click
import pytesseract
from PIL import Image
from pypdf import PageObject, PdfReader

from pdf_cli.commands.utils import Range
from pdf_cli.main import main


@main.command()
@click.argument("input_file", type=click.File("rb"))
@click.option("-p", "--pages", default=None, type=Range, help="starting page to extract")
@click.option("-o", "--output", type=click.File("wb"), required=False, help="output file")
@click.option("-v", "--verbosity", type=int, default=0)
@click.option("-r", "--rotate", type=click.Choice(["left", "right", "inverted"]), default="left")
def ocr(
    input_file: click.File,
    output: "click.File | None",
    pages: list[int],
    verbosity: int,
    **kwargs: Any,  # noqa: ARG001
) -> None:
    """Extract text from PDF using OCR"""
    source = PdfReader(input_file)  # type: ignore[arg-type]

    if pages is None:
        pages = Range(f"1-{len(source.pages)}", None)
    if output is None:
        output = click.File("wb")(Path(input_file.name).with_suffix(".txt"), None)

    extracted_text = ""

    for page_num in pages:
        if page_num > len(source.pages):
            raise click.UsageError("Page number out of range")
        real_page = page_num - 1
        page: PageObject = source.pages[real_page]
        if verbosity >= 2:
            click.echo(f"Extracting page {page_num}")
        elif verbosity >= 1:
            click.echo(".", nl=False)
        extracted_text += page.extract_text()
        for img in page.images:
            image = Image.open(io.BytesIO(img.data))
            extracted_text += pytesseract.image_to_string(image)

    output.write(extracted_text.encode("utf-8"))  # type: ignore[union-attr]
