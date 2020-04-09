import glob
from pathlib import Path

import pytest
from click.testing import CliRunner
from pdf_cli.main import main


@pytest.mark.parametrize("verbosity", [0, 1])
def test_watermark(verbosity):
    runner = CliRunner()
    with runner.isolated_filesystem() as dir:
        result = runner.invoke(main, ['watermark',
                                      str(Path(__file__).parent / 'data/sample.pdf'),
                                      str(Path(__file__).parent / 'data/sample.pdf'),
                                      '-v', verbosity,
                                      '-o', 'output.pdf'])
        assert result.exit_code == 0, result.output
        assert (Path(dir) / 'output.pdf').exists()
