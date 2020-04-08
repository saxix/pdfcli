import glob
from pathlib import Path

import pytest
from click.testing import CliRunner
from pdf_cli.main import main


@pytest.mark.parametrize("verbosity", [0, 1])
def test_join_all(verbosity):
    runner = CliRunner()
    with runner.isolated_filesystem() as dir:
        result = runner.invoke(main, ['join',
                                      *glob.glob(str(Path(__file__).parent / 'data/p*.pdf')),
                                      '-v', verbosity,
                                      '-o', 'output.pdf'])
        assert result.exit_code == 0, result.output
        assert (Path(dir) / 'output.pdf').exists()

@pytest.mark.parametrize("verbosity", [0, 1])
def test_join_no_glob(verbosity):
    runner = CliRunner()
    with runner.isolated_filesystem() as dir:
        result = runner.invoke(main, ['join',
                                      *glob.glob(str(Path(__file__).parent / 'data/xx*.pdf')),
                                      '-v', verbosity,
                                      '-o', 'output.pdf'])
        assert result.exit_code == 1, result.output

@pytest.mark.parametrize("verbosity", [0, 1])
def test_join_file_does_not_exist(verbosity):
    runner = CliRunner()
    with runner.isolated_filesystem() as dir:
        result = runner.invoke(main, ['join',
                                      'error.pdf',
                                      '-o', 'output.pdf',
                                      '-v', verbosity,
                                      ])
        assert result.exit_code == 1, result.output

@pytest.mark.parametrize("verbosity", [0, 1])
def test_join_file_not_fount(verbosity):
    runner = CliRunner()
    with runner.isolated_filesystem() as dir:
        result = runner.invoke(main, ['join',
                                      str(Path(__file__).parent / 'data/page-01.pdf'),
                                      'error.pdf',
                                      '-o', 'output.pdf',
                                      '-v', verbosity,
                                      ])
        assert result.exit_code == 1, result.output

#
# def test_split_range2():
#     runner = CliRunner()
#     with runner.isolated_filesystem() as dir:
#         result = runner.invoke(main, ['split',
#                                       str(Path(__file__).parent / 'sample.pdf'),
#                                       '-p', '1,3'])
#         assert not (Path(dir) / 'page-00.pdf').exists()
#         assert (Path(dir) / 'page-01.pdf').exists()
#         assert not (Path(dir) / 'page-02.pdf').exists()
#         assert (Path(dir) / 'page-03.pdf').exists()
#
#
# def test_split_output_dir():
#     runner = CliRunner()
#     with runner.isolated_filesystem() as dir:
#         result = runner.invoke(main, ['split',
#                                       str(Path(__file__).parent / 'sample.pdf'),
#                                       '-d', 'DEST'])
#         assert (Path(dir) / 'DEST/page-01.pdf').exists()
#         assert (Path(dir) / 'DEST/page-03.pdf').exists()
