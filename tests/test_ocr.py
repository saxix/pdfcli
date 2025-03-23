from pathlib import Path

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
