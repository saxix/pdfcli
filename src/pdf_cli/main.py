import click

@click.group()
def main():
    pass

from . import commands

if __name__ == "__main__":
    main()
