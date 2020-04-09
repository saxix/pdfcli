import glob
from pathlib import Path

import pytest
from click.testing import CliRunner
from pdf_cli.main import main


@pytest.mark.parametrize("verbosity", [0, 1])
def test_encryption_all(verbosity):
    runner = CliRunner()
    with runner.isolated_filesystem() as dir:
        result = runner.invoke(main, ['encrypt',
                                      str(Path(__file__).parent / 'data/sample.pdf'),
                                      '-p', 'password',
                                      '-v', verbosity,
                                      '-o', 'encrypted.pdf'])
        assert result.exit_code == 0, result.output
        assert (Path(dir) / 'encrypted.pdf').exists()

        result = runner.invoke(main, ['decrypt',
                                      'encrypted.pdf',
                                      '-p', 'password',
                                      '-v', verbosity,
                                      '-o', 'decrypted.pdf'])
        assert result.exit_code == 0, result.output
        assert (Path(dir) / 'decrypted.pdf').exists()

# @pytest.mark.parametrize("verbosity", [0, 1])
# def test_join_no_glob(verbosity):
#     runner = CliRunner()
#     with runner.isolated_filesystem() as dir:
#         result = runner.invoke(main, ['join',
#                                       *glob.glob(str(Path(__file__).parent / 'data/xx*.pdf')),
#                                       '-v', verbosity,
#                                       '-o', 'output.pdf'])
#         assert result.exit_code == 1, result.output
#
# @pytest.mark.parametrize("verbosity", [0, 1])
# def test_join_file_does_not_exist(verbosity):
#     runner = CliRunner()
#     with runner.isolated_filesystem() as dir:
#         result = runner.invoke(main, ['join',
#                                       'error.pdf',
#                                       '-o', 'output.pdf',
#                                       '-v', verbosity,
#                                       ])
#         assert result.exit_code == 1, result.output
#
# @pytest.mark.parametrize("verbosity", [0, 1])
# def test_join_file_not_fount(verbosity):
#     runner = CliRunner()
#     with runner.isolated_filesystem() as dir:
#         result = runner.invoke(main, ['join',
#                                       str(Path(__file__).parent / 'data/page-01.pdf'),
#                                       'error.pdf',
#                                       '-o', 'output.pdf',
#                                       '-v', verbosity,
#                                       ])
#         assert result.exit_code == 1, result.output
#
