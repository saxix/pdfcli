from __future__ import annotations

import io
from pathlib import Path
from typing import Any

import click
import pytesseract
from cloup import option, option_group
from cloup.constraints import mutually_exclusive
from PIL import Image
from pypdf import PageObject, PdfReader
from pytesseract import TesseractNotFoundError

from pdf_cli.main import main
from pdf_cli.utils import Console, Range, check_or_create_destination, formatter_settings


@main.command(formatter_settings=formatter_settings)
@click.argument("input_file", type=click.File("rb"))
@click.option("-p", "--pages", default=None, type=Range, help="pages to extract")
@click.option("-v", "--verbosity", type=int, default=1, help="verbosity level")
@option_group(
    "Color options",
    option(
        "-d",
        "--destination",
        "destination",
        type=click.Path(exists=False),
        help="destination directory to create extracted files",
    ),
    option("-o", "--output", type=click.File("wb"), required=False, help="output file"),
    constraint=mutually_exclusive,
)
@click.option("-f", "--format", "fmt", default="page-%02d.txt", help="page filename pattern")
def ocr(
    input_file: click.File,
    output: "click.File | None",
    destination: "click.Path | None",
    pages: list[int] | None = None,
    fmt: str = "page-%02d.pdf",
    verbosity: int = 1,
    **kwargs: Any,  # noqa: ARG001
) -> None:
    """Extract text from PDF using OCR"""

    console = Console(verbosity)
    source = PdfReader(input_file)  # type: ignore[arg-type]
    if pages is None:
        pages = Range(f"1-{len(source.pages)}", None)
    if destination:
        destination = check_or_create_destination(destination)
    elif output is None:
        output = click.File("wb")(Path(input_file.name).with_suffix(".txt"), None)

    extracted_text = []
    for page_num in pages:
        if page_num > len(source.pages):
            console.info(f"Page number {page_num} out of range. Ignored", fg="red", err=True)
            continue
        real_page = page_num - 1
        page: PageObject = source.pages[real_page]
        console.echo(".", f"Extracting page {page_num}")
        page_text = page.extract_text()
        for img in page.images:
            image = Image.open(io.BytesIO(img.data))
            try:
                page_text += pytesseract.image_to_string(image)
            except TesseractNotFoundError:
                raise click.UsageError("Tesseract not found") from None
        extracted_text.append(page_text)
    console.info("")

    if destination:
        for page_num, part in enumerate(extracted_text, 1):
            dest_file = (destination / Path(fmt % page_num)).absolute()
            with dest_file.open("w") as f:
                f.write(part)
            console.info(f"Content extracted to {dest_file.name}")
    else:
        output.write("".join(extracted_text).encode("utf-8"))  # type: ignore[union-attr]
        console.info(f"Content extracted to {output.name}")
