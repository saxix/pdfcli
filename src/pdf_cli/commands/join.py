from typing import Any

import click
from pypdf import PdfReader, PdfWriter

from pdf_cli.main import main


@main.command()
@click.argument("inputs", nargs=-1, type=click.Path(exists=True))
@click.option("-o", "--output", type=click.File("wb"), required=True)
@click.option("-v", "--verbosity", type=int, default=0)
def join(inputs: list[str], output: click.File, verbosity: int, **kwargs: Any) -> None:  # noqa: ARG001
    """join multiple pdf together in a single file."""

    out = PdfWriter()

    for input_file in inputs:
        source = PdfReader(input_file)
        if verbosity >= 1:
            click.echo(f"Adding {input_file}")
        for page_num in range(len(source.pages)):
            out.add_page(source.pages[page_num])

    out.write(output)  # type: ignore[arg-type]
    if verbosity >= 1:
        click.echo(f"Writing {output.name}")
