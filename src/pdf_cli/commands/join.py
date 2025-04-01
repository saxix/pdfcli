from __future__ import annotations

from typing import Any

import click
from pypdf import PdfReader, PdfWriter

from pdf_cli.main import main
from pdf_cli.utils import Console


@main.command()
@click.argument("inputs", nargs=-1, type=click.Path(exists=True))
@click.option("-o", "--output", type=click.File("wb"), required=True)
@click.option("-v", "--verbosity", type=int, default=0)
def join(inputs: list[str], output: click.File, verbosity: int, **kwargs: Any) -> None:  # noqa: ARG001
    """join multiple pdf together in a single file."""

    out = PdfWriter()
    console = Console(verbosity)

    for input_file in inputs:
        source = PdfReader(input_file)
        console.echo(".", f"Adding page {input_file}")
        for page_num in range(len(source.pages)):
            out.add_page(source.pages[page_num])

    out.write(output)  # type: ignore[arg-type]
    console.info(f"Writing {output.name}")
