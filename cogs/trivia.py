import asyncio
import json
import random

from discord.ext import commands
from typing import Dict


class Trivia:
    """A guessing game based on chemical formulas.
    
    Attributes:
        bot (commands.Bot): the bot

        CHEM_DATA (Dict[str, str]): Chemical name -> notation
    """
    with open('data/chem.json') as f:
        CHEM_DATA = json.load(f)

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def trivia(self, ctx):
        """Start a guessing game for chemical compositions.

        SciBo will ask you the chemical notation for a random chemical.
        If you guess it, you get a point!
        """
        rand_key = random.choice(list(self.CHEM_DATA))
        answer = self.CHEM_DATA[rand_key]

        await ctx.send('Trivia Started!')
        await ctx.send(f'What is the chemical composition for {rand_key}?')

        async def on_message(message):
            """Collect the messages"""
            if message.content == answer:
                return await ctx.send(f'Correct! {message.author.mention}. The answer was `{answer}`.')

def setup(bot):
    bot.add_cog(Trivia(bot))
