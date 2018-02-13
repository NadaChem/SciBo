import discord
from discord.ext import commands
import asyncio

from utils.misc import shell, no_codeblock
from io import StringIO
import contextlib
import traceback


class Owner:
    """Owner-only commands."""

    def __local_check(self, ctx):
        return ctx.author.id in [142033635443343360, 121678432504512512]

    def cleanup_code(self, content):
        """Automatically removes code blocks from the code."""
        if content.startswith('```') and content.endswith('```'):
            return '\n'.join(content.split('\n')[1:-1])

        return content.strip('` \n')

    def get_syntax_error(self, e):
        """Returns the syntax error in formatted form."""
        if e.text is None:
            return f'```py\n{e.__class__.__name__}: {e}\n```'
        return f'```py\n{e.text}{"^":>{e.offset}}\n{e.__class__.__name__}: {e}```'

    @commands.command(hidden=True)
    async def load(self, ctx, *, _module):
        """Loads a module."""
        try:
            ctx.bot.load_extension(_module)
        except Exception as e:
            await ctx.send(str(e).capitalize())
        else:
            await ctx.message.add_reaction('\N{OK HAND SIGN}')

    @commands.command(hidden=True)
    async def unload(self, ctx, *, _module):
        """Unloads a module."""
        try:
            ctx.bot.unload_extension(_module)
        except Exception as e:
            await ctx.send(str(e).capitalize())
        else:
            await ctx.message.add_reaction('\N{OK HAND SIGN}')

    @commands.command(name='reload', hidden=True)
    async def _reload(self, ctx, *, _module):
        """Reloads a module."""
        _module = f'cogs.{_module}'
        try:
            ctx.bot.unload_extension(_module)
            ctx.bot.load_extension(_module)
        except Exception as e:
            await ctx.send(str(e).capitalize())
        else:
            await ctx.message.add_reaction('\N{OK HAND SIGN}')

    @commands.command(name='eval', hidden=True)
    async def _eval(self, ctx, *, code: no_codeblock):
        """Evaluates code."""

        code = code.lstrip("`").rstrip("`")
        lines = code.split("\n")
        lines = ["    " + i for i in lines]
        lines = '\n'.join(lines)

        f_code = f"async def _():\n{lines}"
        stdout = StringIO()

        try:
            namespace = {
                "ctx": ctx,
                "message": ctx.message,
                "guild": ctx.message.guild,
                "channel": ctx.message.channel,
                "author": ctx.message.author,
                "bot": ctx.bot
            }
            exec(f_code, namespace, namespace)
            func = namespace["_"]

            with contextlib.redirect_stdout(stdout):
                result = await func()

        except Exception as e:
            result = ''.join(traceback.format_exception(None, e, e.__traceback__))
        finally:
            stdout.seek(0)

        fmt = f"{stdout.read()}\n{result}\n"

        e = discord.Embed(name='Eval', colour=discord.Colour.blurple())
        e.add_field(name='Input:', value=f'```py\n{code}```')
        e.add_field(name='Output:', value=f'```py\n{fmt}```')
        msg = await ctx.send(embed=e)
        await asyncio.sleep(10)
        e.remove_field(0)
        await msg.edit(embed=e)

    @commands.command(name='sh', typing=True, hidden=True)
    async def shell(self, ctx, *, cmd: no_codeblock):
        """Run a subprocess using shell."""
        result = await shell(cmd)
        e = discord.Embed(name='Shell', colour=discord.Colour.blurple())
        e.add_field(name='Input:', value=f'```cmd\n{cmd}```')
        e.add_field(name='Output:', value=f'```cmd\n{result}```')
        msg = await ctx.send(embed=e)
        await asyncio.sleep(10)
        e.remove_field(0)
        await msg.edit(embed=e)


def setup(bot):
    bot.add_cog(Owner())
