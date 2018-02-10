import asyncio
import random

from typing import Union


class Game:
    def __init__(self, ctx, *, limit: Union[int, None]):
        self.ctx = ctx
        self.bot = ctx.bot
        self.loop = ctx.bot.loop
        self.guild_id = ctx.guild.id
        self.count = 0
        self.limit = limit
        self.task = self.loop.create_task(self.trivia_task())

    async def trivia_task(self):
        while not self.bot.is_closed():
            rand_key = random.choice(list(self.bot.CHEM_DATA))
            answer = self.bot.CHEM_DATA[rand_key]

            await self.ctx.send(f"What is the chemical composition for `{rand_key}`? You've got 30 seconds.")

            # Collect messages
            while True:
                try:
                    message = await self.bot.wait_for('message', timeout=30.0)
                except asyncio.TimeoutError:
                    await self.ctx.send(f"Time's up! The answer was `{answer}`.")

                if message.content == answer:
                    await self.ctx.send(f'Correct! {message.author.mention}. The answer was `{answer}`.')
                    break

            # Increment the question counter
            self.count += 1
            if self.count > self.limit:
                return self.stop()

            await self.ctx.send('Next question in 10 seconds!')
            await asyncio.sleep(10)

    async def stop(self):
        if not self.task.cancelled():
            await self.ctx.send(f"Fun's over! You answered {self.count} questions.")
            return self.task.cancel()

        await self.ctx.send("You don't have any active games running.")
        raise asyncio.CancelledError(f'Game for guild {self.guild_id} has already stopped.')

    def __repr__(self) -> str:
        return '<Guild id={0.guild_id!r} limit={0.limit!r}>'.format(self)

    def __eq__(self, other) -> bool:
        return isinstance(other, Game) and self.guild_id == other.guild_id
