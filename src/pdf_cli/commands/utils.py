from typing import TYPE_CHECKING, Any

import click

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
