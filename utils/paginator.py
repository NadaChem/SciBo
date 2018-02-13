import discord
from discord.ext import commands
import typing
import asyncio
import math


class Field:
    """Custom class which emulates a field of an embed."""
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __lt__(self, other):
        return self.name < other.name

    def __repr__(self):
        return f'<Field name={self.name!r} value={self.value!r}>'


def shorten(text):
    """Shortens width of text."""
    text = text.split("\n", 1)[0]
    if len(text) > 50:
        return text[:50 - 3] + '...'
    return text


def make_embed(fields: typing.List[Field]):
    """Makes an embed from a list of Field."""
    e = discord.Embed(colour=discord.Colour.blurple())
    for i in range(5):
        try:
            e.add_field(name=fields[i].name, value=shorten(fields[i].value), inline=False)
        except IndexError:
            pass
    return e


class Paginator:
    """Main Paginator class for pagination."""
    def __init__(self, ctx: commands.Context, fields: typing.List[Field], *, description: str):
        self.ctx = ctx
        self.msg = None
        self.fields = fields
        self.description = description
        self.total_pages = math.ceil(len(fields) / 5) - 1
        self.current_page = 0
        self.em_list = []
        self.running = False
        self.match = None
        self.BUTTON_FIRST = "⏪"
        self.BUTTON_BACKWARDS = "⬅"
        self.BUTTON_STOP = "⏹"
        self.BUTTON_FORWARD = "➡"
        self.BUTTON_LAST = "⏩"

        for i in range(round(len(fields) / 5)):
            self.em_list.append(make_embed(fields[i*5:]))

    async def send_page(self):
        """Sends the current page according to `self.current_page`."""
        em = self.em_list[self.current_page]
        em.description = self.description
        em.set_footer(text=f'{self.current_page + 1}/{self.total_pages + 1}', icon_url=self.ctx.bot.user.avatar_url)

        if self.msg is None:
            self.msg = await self.ctx.send(embed=em)
        else:
            await self.msg.edit(embed=em)

    async def init_reactions(self):
        """Adds the initial reactions to this message."""
        add_reactions = [self.BUTTON_STOP]

        if self.total_pages != 0:
            add_reactions.insert(0, self.BUTTON_BACKWARDS)
            add_reactions.append(self.BUTTON_FORWARD)

        if self.total_pages > 1:
            add_reactions.insert(0, self.BUTTON_FIRST)
            add_reactions.append(self.BUTTON_LAST)

        for reaction in add_reactions:
            await self.msg.add_reaction(reaction)

    def check(self, reaction, user):
        """Reaction and user check for the button selector."""
        valid_emojis = [self.BUTTON_FIRST,
                        self.BUTTON_BACKWARDS,
                        self.BUTTON_STOP,
                        self.BUTTON_FORWARD,
                        self.BUTTON_LAST]
        if user.id != self.ctx.author.id:
            return

        if reaction.message.id != self.msg.id:
            return

        if reaction.emoji in valid_emojis:
            self.match = reaction.emoji
            return True

    async def paginate(self):
        """Main pagination function that basically controls the paginator."""
        self.running = True
        await self.send_page()
        await self.init_reactions()

        while self.running:
            try:
                reaction, user = await self.ctx.bot.wait_for('reaction_add', check=self.check, timeout=120.0)
            except asyncio.TimeoutError:
                self.running = False
                await self.msg.delete()
                break

            try:
                await self.msg.remove_reaction(reaction, user)
            except Exception as e:
                await self.ctx.send(e)

            if self.match == self.BUTTON_FIRST:
                if self.current_page != 0:
                    self.current_page = 0
                    await self.send_page()

            if self.match == self.BUTTON_FORWARD:
                if self.current_page < self.total_pages:
                    self.current_page += 1
                else:
                    self.current_page = 0
                await self.send_page()

            if self.match == self.BUTTON_STOP:
                await self.msg.delete()
                break

            if self.match == self.BUTTON_BACKWARDS:
                if self.current_page > 0:
                    self.current_page -= 1
                else:
                    self.current_page = self.total_pages - 1

                await self.send_page()

            if self.match == self.BUTTON_LAST:
                if self.total_pages != self.current_page:
                    self.current_page = self.total_pages
                    await self.send_page()
