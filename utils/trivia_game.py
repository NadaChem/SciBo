import asyncio
import random
import time

from typing import Union


class Game:
    """A class representing a ScIeNtiFic trivia game

    Attributes:
        ctx: The context in which the command was called
        bot: The discord.ext.commands.Bot instance currently running
        loop: The bot's asyncio loop
        guild_id: The server id of in which the :class:`Game`is currently
            being run
        count: A running tally of how many questions have been asked
        limit: The # of questions to be asked in total (can be None for unlimited)
        task: :meth:`trivia_task`
        skip_question (bool): whether to skip a question.

    Args:
        ctx: The context in which the command was called (passed from the cog)
        limit: The # of questions to be asked (passed from cog)
    """

    def __init__(self, ctx, *, limit: Union[int, None]):
        self.ctx = ctx
        self.bot = ctx.bot
        self.loop = ctx.bot.loop
        self.guild_id = ctx.guild.id
        self.count = 0
        self.limit = limit
        self.task = self.loop.create_task(self.trivia_task())
        self.answer = None
        self.skip_question = False

    async def trivia_task(self):
        """The trivia task.
        Runs the trivia game in a loop.
        Exits if stop() is called, or if the limit of the game is reached."""
        while not self.bot.is_closed():
            rand_key = random.choice(list(self.bot.CHEM_DATA))
            self.answer = self.bot.CHEM_DATA[rand_key]

            await self.ctx.send(f"What is the chemical composition for `{rand_key}`? You've got 30 seconds.")
            start_time = time.time()

            # Collect messages
            await self.get_input(start_time)

            # Increment the question counter
            self.count += 1
            if self.limit is not None:
                if self.count > self.limit:
                    return self.stop()

            # Less spammy
            await asyncio.sleep(3)

            await self.ctx.send('Next question in 10 seconds!')
            await asyncio.sleep(10)

    async def stop(self):
        """Stops the asyncio trivia task"""
        if not self.task.cancelled():
            await self.ctx.send(f"Fun's over! You answered `{self.count}` question(s).")
            return self.task.cancel()

        await self.ctx.send("You don't have any active games running.")
        raise asyncio.CancelledError(f'Game for guild {self.guild_id} has already stopped.')

    def check(self, message):
        if message.channel != self.ctx.channel:
            return False

        if message.author.bot:
            return False

        if message.content.lower() == 'skip':
            self.skip_question = True
        
        return True

    async def get_input(self, start_time):
        while True:
            message = await self.bot.wait_for('message', check=self.check)

            if self.skip_question:
                await self.ctx.send(f'Skipped! The answer was `{self.answer}`')
                break

            if message.content.lower() == self.answer.lower():
                await self.ctx.send(f'Correct! {message.author.mention} The answer was `{self.answer}`.')
                break

            if time.time() - start_time > 30:
                await self.ctx.send(f"Time's up! The answer was `{self.answer}`.")
                break

    def __repr__(self) -> str:
        return '<Guild id={0.guild_id!r} limit={0.limit!r}>'.format(self)

    def __eq__(self, other) -> bool:
        return isinstance(other, Game) and self.guild_id == other.guild_id
