from __future__ import annotations

from pathlib import Path
from typing import Any

import click
from pypdf import PdfReader, PdfWriter

from pdf_cli.main import main
from pdf_cli.utils import Console, Range


@main.command()
@click.argument("input_file", type=click.File("rb"))
@click.option("-p", "--pages", default=None, type=Range, help="starting page to extract")
@click.option("-f", "--format", "fmt", default="page-%02d.pdf", help="page filename pattern")
@click.option("-d", "--destination", type=click.Path(exists=False), default=".")
@click.option("-v", "--verbosity", type=int, default=0)
def split(
    input_file: click.File,
    destination: click.Path,
    pages: list[int] | None,
    fmt: str,
    verbosity: int,
    **kwargs: Any,  # noqa: ARG001
) -> None:
    """split pdf into multiple single page file."""
    console = Console(verbosity)
    source = PdfReader(input_file)  # type: ignore[arg-type]
    if pages is None:
        pages = Range(f"1-{len(source.pages)}", None)

    to_dir = Path(destination)  # type: ignore[arg-type]
    if not to_dir.exists():
        to_dir.mkdir(parents=True)

    for page_num in pages:
        real_page = page_num - 1
        console.echo(".", f"Extracting page {page_num}")
        # due to a bug PyPDF4 file need to be reopened
        source = PdfReader(input_file)  # type: ignore[arg-type]
        dest_file = (to_dir / Path(fmt % page_num)).absolute()
        page = source.pages[real_page]
        output_pdf = PdfWriter()
        output_pdf.add_page(page)
        with dest_file.open("wb") as f:
            output_pdf.write(f)
            console.info(f"Writing {output_pdf}")
