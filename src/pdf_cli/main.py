import click


@click.group(invoke_without_command=True)
@click.option('--version', is_flag=True, default=False)
def main(version):
    if version:
        import pkg_resources
        VERSION = pkg_resources.require("pdf_cli")[0].version
        click.echo(VERSION)


from . import commands

if __name__ == "__main__":
    main()
