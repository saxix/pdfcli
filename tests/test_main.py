from click.testing import CliRunner

from pdf_cli.main import main


def test_main():
    runner = CliRunner()
    result = runner.invoke(main)
    assert result.exit_code == 0


def test_version():
    runner = CliRunner()
    result = runner.invoke(main, "--version")
    assert result.exit_code == 0
