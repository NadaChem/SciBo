from discord.ext import commands

from .paginator import Paginator


class SciBoContext(commands.Context):

    async def paginate(self, *args, **kwargs):
        """Makes an interactive paginated embed."""
        return await Paginator(self, *args, **kwargs).paginate()
