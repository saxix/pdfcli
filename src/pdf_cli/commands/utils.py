import click


class RangeParamType(click.ParamType):
    name = "range"

    def convert(self, value, param, ctx):
        ranges = value.split(',')
        selection = []
        try:
            for r in ranges:
                if '-' in r:
                    s, e = r.split('-')
                    for num in range(int(s.strip()), int(e.strip())+1):
                        selection.append(num)
                else:
                    selection.append(int(r))
            return selection
        except (TypeError, ValueError) as e:
            self.fail(
                "invalid range format: uses from-to,page,from-to "
                f"{e!r} of type {type(e).__name__}",
                param,
                ctx,
            )


Range = RangeParamType()
