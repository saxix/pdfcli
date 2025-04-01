import os
from pathlib import Path
from unittest.mock import patch

import pytest
from click.testing import CliRunner

from pdf_cli.main import main


@pytest.mark.parametrize("pages", ["1", "1-2", "1,3"])
@pytest.mark.parametrize("verbosity", [0, 1, 2])
def test_extract_all(verbosity, pages):
    runner = CliRunner()
    with runner.isolated_filesystem() as dir:
        result = runner.invoke(
            main,
            [
                "ocr",
                str(Path(__file__).parent / "data/ocr.pdf"),
                "-v",
                verbosity,
                "-p",
                pages,
                "-o",
                "output.txt",
            ],
        )
        assert result.exit_code == 0, result.output
        assert (Path(dir) / "output.txt").exists()


def test_join_no_glob():
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(
            main, ["ocr", str(Path(__file__).parent / "data/ocr.pdf")]
        )
        assert result.exit_code == 0, result.output
        assert (Path(__file__).parent / "data/ocr.txt").exists()


def test_extract_out_of_range():
    runner = CliRunner()
    with runner.isolated_filesystem() as dir:
        result = runner.invoke(
            main,
            [
                "ocr",
                str(Path(__file__).parent / "data/ocr.pdf"),
                "-p",
                "99",
                "-o",
                "output.txt",
            ],
        )
        assert result.exit_code == 0, result.output
        assert "Page number 99 out of range. Ignored" in result.output
        assert "Content extracted to output.txt" in result.output
        assert (Path(dir) / "output.txt").exists()


@pytest.mark.parametrize("verbosity", [0, 1, 2])
def test_extract_multiple(verbosity):
    runner = CliRunner()
    with runner.isolated_filesystem() as dir:
        result = runner.invoke(
            main,
            [
                "ocr",
                str(Path(__file__).parent / "data/ocr.pdf"),
                "-v",
                verbosity,
                "-d",
                "output/",
            ],
        )
        assert result.exit_code == 0, result.output
        assert not (Path(dir) / "output.txt").exists()
        assert (Path(dir) / "output/page-01.txt").exists()


def test_extract_destination_not_empty():
    runner = CliRunner()
    with runner.isolated_filesystem() as dir:
        (Path(dir) / "aaaa").mkdir()
        result = runner.invoke(
            main,
            [
                "ocr",
                str(Path(__file__).parent / "data/ocr.pdf"),
                "-v",
                "2",
                "-d",
                "aaaa",
            ],
        )
        assert result.exit_code == 0, result.output
        assert (Path(dir) / "aaaa/page-01.txt").exists()



def test_error_extract_destination_not_empty():
    runner = CliRunner()
    with runner.isolated_filesystem() as dir:
        (Path(dir) / "aaaa").mkdir()
        (Path(dir) / "aaaa" / "file1").touch()
        result = runner.invoke(
            main,
            [
                "ocr",
                str(Path(__file__).parent / "data/ocr.pdf"),
                "-v",
                "2",
                "-d",
                "aaaa",
            ],
        )
        assert result.exit_code == 2, result.output
        assert "Error: destination directory already exists and it is not empty" in result.output


def test_error_extract_destination_is_file():
    runner = CliRunner()
    with runner.isolated_filesystem() as dir:
        (Path(dir) / "aaaa").mkdir()
        (Path(dir) / "aaaa" / "file1").touch()
        result = runner.invoke(
            main,
            [
                "ocr",
                str(Path(__file__).parent / "data/ocr.pdf"),
                "-v",
                "2",
                "-d",
                "aaaa/file1",
            ],
        )
        assert result.exit_code == 2, result.output
        assert "Error: destination is a file" in result.output



def test_error_tesseract_not_fount(monkeypatch):
    runner = CliRunner()
    monkeypatch.setenv("PATH", "")
    with patch.dict(os.environ, {}):
        with runner.isolated_filesystem() as dir:
            result = runner.invoke(
                main,
                [
                    "ocr",
                    str(Path(__file__).parent / "data/ocr.pdf"),
                    "-v",
                    "2",
                    "-d",
                    "output",
                ],
            )
            assert result.exit_code == 2, result.output
            assert "Error: Tesseract not found" in result.output
