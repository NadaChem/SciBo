import asyncio
import traceback
import inspect

import discord

from discord.ext import commands
from utils.misc import shell, no_codeblock


class Owner:
    """Owner-only commands"""

    def __local_check(self, ctx):
        return ctx.author.id in [142033635443343360, 121678432504512512]

    def cleanup_code(self, content):
        """Automatically removes code blocks from the code."""
        if content.startswith('```') and content.endswith('```'):
            return '\n'.join(content.split('\n')[1:-1])

        return content.strip('` \n')

    def get_syntax_error(self, e):
        if e.text is None:
            return f'```py\n{e.__class__.__name__}: {e}\n```'
        return f'```py\n{e.text}{"^":>{e.offset}}\n{e.__class__.__name__}: {e}```'

    @commands.command(hidden=True)
    async def load(self, ctx, *, _module):
        """Loads a module."""
        try:
            ctx.bot.load_extension(_module)
        except Exception as e:
            await ctx.send(f'```py\n{traceback.format_exc()}\n```')
        else:
            await ctx.send('\N{OK HAND SIGN}')

    @commands.command(hidden=True)
    async def unload(self, ctx, *, _module):
        """Unloads a module."""
        try:
            ctx.bot.unload_extension(_module)
        except Exception as e:
            await ctx.send(f'```py\n{traceback.format_exc()}\n```')
        else:
            await ctx.send('\N{OK HAND SIGN}')

    @commands.command(name='reload', hidden=True)
    async def _reload(self, ctx, *, _module):
        """Reloads a module."""
        try:
            ctx.bot.unload_extension(_module)
            ctx.bot.load_extension(_module)
        except Exception as e:
            await ctx.send(f'```py\n{traceback.format_exc()}\n```')
        else:
            await ctx.send('\N{OK HAND SIGN}')

    @commands.command(name='eval')
    async def _eval(self, ctx, *, body: no_codeblock):
        """Evaluates code
        Credits: Rapptz/RoboDanny"""

        env = {
            'bot': ctx.bot,
            'ctx': ctx,
            'channel': ctx.channel,
            'guild': ctx.guild,
            'message': ctx.message,
            'prefix': ctx.prefix
        }

        try:
            result = eval(body, env)
            if inspect.isawaitable(result):
                result = await result
        except Exception as e:
            result = str(e)
        else:
            if not isinstance(result, str):
                result = repr(result) if result is not None else 'No Result'

        e = discord.Embed(name='Eval', colour=discord.Colour.blurple())
        e.add_field(name='Input:', value=f'```py\n{body}```')
        e.add_field(name='Output:', value=f'```py\n{result}```')
        msg = await ctx.send(embed=e)
        await asyncio.sleep(10)
        e.remove_field(0)
        await msg.edit(embed=e)

    @commands.command(name='sh', typing=True)
    async def shell(self, ctx, *, cmd: no_codeblock):
        """Run a subprocess using shell."""
        result = await shell(cmd)
        e = discord.Embed(name='Shell', colour=discord.Colour.blurple())
        e.add_field(name='Input:', value=f'```py\n{cmd}```')
        e.add_field(name='Output:', value=f'```py\n{result}```')
        msg = await ctx.send(embed=e)
        await asyncio.sleep(10)
        e.remove_field(0)
        await msg.edit(embed=e)


def setup(bot):
    bot.add_cog(Owner())
