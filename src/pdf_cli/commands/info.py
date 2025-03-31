from typing import Any

import click
from pypdf import PdfReader

from pdf_cli.main import main


@main.command()
@click.argument("input_file", type=click.File("rb"))
@click.option("-v", "--verbosity", type=int, default=0)
def info(input_file: click.File, **kwargs: Any) -> None:  # noqa: ARG001
    """dump pdf information."""

    pdf = PdfReader(input_file)  # type: ignore[arg-type]
    information: dict[str, Any] = pdf._info or {}
    number_of_pages = len(pdf.pages)
    txt = f"""Filename: {input_file.name}
Author: {information.get("/Author", "")}
Creator: {information.get("/Creator", "")}
Date: {information.get("/CreationDate", "")}
Producer: {information.get("/Producer", "")}
Subject: {information.get("/Subject", "")}
Title: {information.get("/Title", "")}
Number of pages: {number_of_pages}"""
    click.echo(txt)
