import glob
from pathlib import Path

import pytest
from click.testing import CliRunner
from pdf_cli.main import main


@pytest.mark.parametrize("pages", ['1', '1-2', '1,2'])
@pytest.mark.parametrize("verbosity", [0, 1,2])
def test_rotate_selection(verbosity, pages):
    runner = CliRunner()
    with runner.isolated_filesystem() as dir:
        result = runner.invoke(main, ['rotate',
                                      str(Path(__file__).parent / 'data/sample.pdf'),
                                      '-v', verbosity,
                                      '-p', pages,
                                      '-o', 'output.pdf'])
        assert result.exit_code == 0, result.output
        assert (Path(dir) / 'output.pdf').exists()


@pytest.mark.parametrize("verbosity", [0, 1,2])
def test_rotate_all(verbosity):
    runner = CliRunner()
    with runner.isolated_filesystem() as dir:
        result = runner.invoke(main, ['rotate',
                                      str(Path(__file__).parent / 'data/sample.pdf'),
                                      '-v', verbosity,
                                      '-o', 'output.pdf'])
        assert result.exit_code == 0, result.output
        assert (Path(dir) / 'output.pdf').exists()
