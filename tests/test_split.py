from pathlib import Path

import pytest
from click.testing import CliRunner
from pdf_cli.main import main


@pytest.mark.parametrize("verbosity", [0, 1])
def test_split_all(verbosity):
    runner = CliRunner()
    with runner.isolated_filesystem() as dir:
        result = runner.invoke(main, ['split', str(Path(__file__).parent / 'data/sample.pdf'),
                                      '-v', verbosity,
                                      ])
        assert not (Path(dir) / 'page-00.pdf').exists()
        assert (Path(dir) / 'page-01.pdf').exists()
        assert (Path(dir) / 'page-02.pdf').exists()
        assert (Path(dir) / 'page-03.pdf').exists()


@pytest.mark.parametrize("verbosity", [0, 1])
def test_split_range1(verbosity):
    runner = CliRunner()
    with runner.isolated_filesystem() as dir:
        result = runner.invoke(main, ['split',
                                      str(Path(__file__).parent / 'data/sample.pdf'),
                                      '-p', '1-2',
                                      '-v', verbosity,
                                      ])
        assert not (Path(dir) / 'page-00.pdf').exists()
        assert (Path(dir) / 'page-01.pdf').exists()
        assert (Path(dir) / 'page-02.pdf').exists()

@pytest.mark.parametrize("verbosity", [0, 1])
def test_split_range2(verbosity):
    runner = CliRunner()
    with runner.isolated_filesystem() as dir:
        result = runner.invoke(main, ['split',
                                      str(Path(__file__).parent / 'data/sample.pdf'),
                                      '-v', verbosity,
                                      '-p', '1,3'])
        assert not (Path(dir) / 'page-00.pdf').exists()
        assert (Path(dir) / 'page-01.pdf').exists()
        assert not (Path(dir) / 'page-02.pdf').exists()
        assert (Path(dir) / 'page-03.pdf').exists()


@pytest.mark.parametrize("verbosity", [0, 1])
def test_split_output_dir(verbosity):
    runner = CliRunner()
    with runner.isolated_filesystem() as dir:
        result = runner.invoke(main, ['split',
                                      str(Path(__file__).parent / 'data/sample.pdf'),
                                      '-v', verbosity,
                                      '-d', 'DEST'])
        assert (Path(dir) / 'DEST/page-01.pdf').exists()
        assert (Path(dir) / 'DEST/page-03.pdf').exists()
