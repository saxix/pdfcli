import glob
import sys
from pathlib import Path

import click
from PyPDF4 import PdfFileReader, PdfFileWriter

from pdf_cli.main import main


@main.command()
@click.argument('inputs', nargs=-1)
@click.option('-o', '--output', type=click.File('wb'), required=True)
@click.option('-v', '--verbosity', type=int, default=0)
@click.pass_context
def join(ctx, inputs, output, verbosity, **kwargs):
    "join multiple pdf together in a single file"
    if not inputs:
        click.echo("No input files")
        ctx.exit(1)

    for input in inputs:
        if not Path(input).exists():
            if verbosity >= 1:
                click.echo("File not found '%s'" % input, err=True)
                ctx.exit(1)

    out = PdfFileWriter()

    for input in inputs:
        source = PdfFileReader(input)
        if verbosity >= 1:
            click.echo("Adding %s" % input)
        for page_num in range(0, source.numPages):
            out.addPage(source.getPage(page_num))

    out.write(output)
    if verbosity >= 1:
        click.echo("Writing %s" % output.name)
