import discord
from discord.ext import commands


class Base:
    """Basic commands for any bot to have i.e. info, ping, etc"""

    @commands.command()
    async def info(self, ctx):
        """Get basic information about SciBo"""
        em = discord.Embed(title='SciBo Info')
        em.description = ctx.bot.description
        em.set_thumbnail(url=ctx.bot.user.avatar_url_as(format='png', size=128))
        em.add_field(name='Commands', value='\u2022'.join(sorted([f'{x.name}\n' for x in ctx.bot.commands])))
        em.add_field(name='Prefixes', value='\u2022'.join([f'{x}\n' for x in ctx.bot.prefixes]))

        await ctx.send(embed=em)


def setup(bot):
    bot.add_cog(Base())
