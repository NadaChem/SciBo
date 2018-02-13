import discord
from discord.ext import commands

from datetime import datetime
from utils.paginator import Field


class Base:
    """Basic commands for any bot to have i.e. info, ping, etc"""

    @commands.command()
    async def info(self, ctx):
        """Get basic information about SciBo."""
        em = discord.Embed(title='SciBo Info', colour=discord.Colour.blurple())
        em.description = ctx.bot.description
        em.set_thumbnail(url=ctx.bot.user.avatar_url_as(format='png', size=128))
        em.add_field(name='Prefixes', value='\n'.join([f'\u2022 {x}' for x in ctx.bot.prefixes]))
        em.add_field(name='Uptime', value=str(datetime.now() - ctx.bot.start_time).split('.')[0])
        em.add_field(name='Ping', value=f'{ctx.bot.latency * 1000:.1f}')
        em.add_field(name='Owners', value='\n'.join(['\u2022 naught0#4417', '\u2022 NCPlayz#7941']))
        em.add_field(name='Source', value='https://github.com/NadaChem/SciBo')

        await ctx.send(embed=em)

    @commands.command(name='help')
    async def _help(self, ctx, cmd=None):
        """Shows this message."""
        if not cmd:
            fields = []
            for command in ctx.bot.commands:
                if command.hidden:
                    if ctx.author.id in ctx.bot.owners:
                        fields.append(Field(command.name, command.help))
                        continue
                fields.append(Field(command.name, command.help))

            fields = sorted(fields)
            await ctx.paginate(fields, description=f'**SciBo Help**\n'
                                                   f'To use these commands, do "{ctx.prefix}<command>"\n'
                                                   f'To find out more about a command, do "{ctx.prefix}help <command>"')
        else:
            result = ctx.bot.get_command(cmd)

            if result is None:
                return await ctx.send(f'Command or category `{cmd}` not found.')

            elif isinstance(result, commands.Command):
                usage = ("\n" + result.usage) if result.usage else ""
                e = discord.Embed(description='**SciBo Help**\n'
                                              f'To use the command, do "{ctx.prefix}{result.name}"',
                                  colour=discord.Colour.blurple())
                e.add_field(name=result.name, value=f'{result.help}{usage}')
                e.set_footer(text=f'Help for {result.name}', icon_url=ctx.bot.user.avatar_url)
                await ctx.send(embed=e)


def setup(bot):
    bot.add_cog(Base())
