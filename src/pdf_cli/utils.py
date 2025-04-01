from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Any

import click
from cloup import HelpFormatter, HelpTheme, Style

if TYPE_CHECKING:
    from click import Parameter


class RangeParamType(click.ParamType):
    name = "range"

    def convert(self, value: Any, param: "Parameter | None", ctx: Any) -> list[int]:
        ranges = value.split(",")
        selection: list[int] = []
        try:
            for r in ranges:
                if "-" in r:
                    s, e = r.split("-")
                    selection.extend(range(int(s.strip()), int(e.strip()) + 1))
                else:
                    selection.append(int(r))
        except (TypeError, ValueError) as e:  # pragma: no cover
            self.fail(
                f"invalid range format: uses from-to,page,from-to {e!r} of type {type(e).__name__}",
                param,
                ctx,
            )
        else:
            return selection


Range = RangeParamType()

formatter_settings = HelpFormatter.settings(
    theme=HelpTheme(
        invoked_command=Style(fg="bright_yellow"),
        heading=Style(fg="bright_white", bold=True),
        constraint=Style(fg="magenta"),
        col1=Style(fg="bright_yellow"),
    )
)


def check_or_create_destination(dest: Path | str) -> Path:
    existing = Path(dest)
    if existing.exists():
        if existing.is_file():
            raise click.UsageError("destination is a file")
        if any(existing.iterdir()):
            raise click.UsageError("destination directory already exists and it is not empty")
    to_dir = Path(dest)  # type: ignore[arg-type]
    if not to_dir.exists():
        to_dir.mkdir(parents=True)
    return to_dir


class Console:
    def __init__(self, verbosity: int) -> None:
        self.verbosity = verbosity

    def out(self, message: str, limit: int, **kwargs: Any) -> None:
        if not self.verbosity:
            return
        if self.verbosity >= limit:
            click.secho(message, **kwargs)

    def echo(self, level1: str, level2: str, level3: str = "", **kwargs: Any) -> None:
        if self.verbosity >= 3:
            click.secho(level3 or level2, **kwargs)
        elif self.verbosity >= 2:
            click.secho(level2, **kwargs)
        elif self.verbosity >= 1:
            click.secho(level1, **kwargs)

    def info(self, message: str, **kwargs: Any) -> None:
        self.out(message, limit=1, **kwargs)

    def warning(self, message: str, **kwargs: Any) -> None:
        self.out(message, limit=2, **kwargs)

    def debug(self, message: str, **kwargs: Any) -> None:
        self.out(message, limit=3, **kwargs)
