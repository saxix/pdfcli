from typing import Any

import click
from pypdf import PdfReader, PdfWriter

from pdf_cli.main import main


@main.command()
@click.argument("input_file", type=click.File("rb"))
@click.option("-o", "--output", type=click.File("wb"), required=True)
@click.option("-v", "--verbosity", type=int, default=0)
@click.option("-p", "--password", type=str)
@click.option(
    "-a",
    "--algorithm",
    help="encrypt algorithm. Values may be one of ",
    type=click.Choice(["RC4-40", "RC4-128", "AES-128", "AES-256-R5", "AES-256"]),
)
def encrypt(
    input_file: click.File,
    output: click.File,
    password: str,
    verbosity: int,
    algorithm: str,
    **kwargs: Any,  # noqa: ARG001
) -> None:
    """Add password protection to PDF files.
    Owner and user passwords can be specified, along with a set of user permissions.

    The encryption algorithm used for protecting the file is configurable.

    """

    source = PdfReader(input_file)  # type: ignore[arg-type]
    output_pdf = PdfWriter()
    for page in source.pages:
        output_pdf.add_page(page)

    output_pdf.encrypt(user_password=password, algorithm=algorithm)

    if verbosity >= 1:
        click.echo(f"Writing {output.name}")
    output_pdf.write(output)  # type: ignore[arg-type]
