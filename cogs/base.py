import discord

from datetime import datetime
from discord.ext import commands


class Base:
    """Basic commands for any bot to have i.e. info, ping, etc"""

    @commands.command()
    async def info(self, ctx):
        """Get basic information about SciBo"""
        em = discord.Embed(title='SciBo Info')
        em.description = ctx.bot.description
        em.set_thumbnail(url=ctx.bot.user.avatar_url_as(format='png', size=128))
        em.add_field(name='Commands', value='\n'.join(sorted([f'\u2022 {x.name}' for x in ctx.bot.commands if not x.hidden])))
        em.add_field(name='Prefixes', value='\n'.join([f'\u2022 {x}' for x in ctx.bot.prefixes]))
        em.add_field(name='Uptime', value=str(datetime.now() - ctx.bot.start_time).split('.')[0])
        em.add_field(name='Ping', value=f'{ctx.bot.latency * 1000:.1f}')
        em.add_field(name='Owners', value='\n'.join(['\u2022 naught0#4417', '\u2022 NCPlayz#7941']))
        em.add_field(name='Source', value='[On Github](https://github.com/NadaChem/SciBo)')

        await ctx.send(embed=em)


def setup(bot):
    bot.add_cog(Base())
