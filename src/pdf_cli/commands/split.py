from pathlib import Path
from typing import Any

import click
from pypdf import PdfReader, PdfWriter

from pdf_cli.commands.utils import Range
from pdf_cli.main import main


@main.command()
@click.argument("input_file", type=click.File("rb"))
@click.option("-p", "--pages", default=None, type=Range, help="starting page to extract")
@click.option("--format", "fmt", default="page-%02d.pdf", help="page filename pattern")
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
    source = PdfReader(input_file)  # type: ignore[arg-type]
    if pages is None:
        pages = Range(f"1-{len(source.pages)}", None)

    to_dir = Path(destination)  # type: ignore[arg-type]
    if not to_dir.exists():
        to_dir.mkdir(parents=True)

    for page_num in pages:
        real_page = page_num - 1
        if verbosity >= 2:
            click.echo(f"Extracting page {page_num}")
        elif verbosity >= 1:
            click.echo(".", nl=False)
        # due to a bug PyPDF4 file need to be reopened
        source = PdfReader(input_file)  # type: ignore[arg-type]
        dest_file = (to_dir / Path(fmt % page_num)).absolute()
        page = source.pages[real_page]
        output_pdf = PdfWriter()
        output_pdf.add_page(page)
        with dest_file.open("wb") as f:
            output_pdf.write(f)
