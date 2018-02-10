from discord.ext import commands

from utils.trivia_game import Game


class Trivia:
    """A guessing game based on chemical formulas."""

    @commands.group(invoke_without_subcommand=True)
    async def trivia(self, ctx):
        """Start a guessing game for chemical compositions.

        SciBo will ask you the chemical notation for a random chemical.
        If you guess it, you get a point!
        """
        if ctx.invoked_subcommand is None:
            return await ctx.invoke(ctx.bot.get_command('trivia start'))

    @trivia.command()
    async def start(self, ctx, limit: int = None):
        """Starts chemically induced trivia."""
        # Make sure only one game is running per guild
        current_game = Game(ctx, limit=limit)
        if current_game in ctx.bot.RUNNING_GAMES:
            return await ctx.send('A game is already running.')
        ctx.bot.RUNNING_GAMES[ctx.guild.id] = current_game

        if limit:
            return await ctx.send(f'Trivia Started! ({limit} question(s))')

        await ctx.send('Trivia Started! (No limit)')

    @trivia.command()
    async def stop(self, ctx):
        """Stops currently running trivia game."""
        if ctx.guild.id not in ctx.bot.RUNNING_GAMES:
            return await ctx.send("This server doesn't have a game running right now.")

        await ctx.bot.RUNNING_GAMES[ctx.guild.id].stop()
        del ctx.bot.RUNNING_GAMES[ctx.guild.id]


def setup(bot):
    bot.add_cog(Trivia)
