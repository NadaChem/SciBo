import json
import traceback
from datetime import datetime
from pathlib import Path

from discord.ext import commands


class SciBo(commands.Bot):
    """Holds some info and junk"""
    with open('data/chem.json') as f:
        CHEM_DATA = json.load(f)

    # The idea here is to store :class:`Game` objects in here
    # to see whether a guild already has a trivia game running
    RUNNING_GAMES = {}

    def __init__(self):
        self.description = 'A scientific bot that does science-y things'
        self.start_time = datetime.now()
        self.startup_cogs = [x.stem for x in Path('cogs').glob('*.py')]
        with open('data/keys.json') as f:
            self.token = json.load(f)['discord']

        self.prefixes = ["sci>", "SciBo "]
        super().__init__(command_prefix=commands.when_mentioned_or(*self.prefixes), description=self.description,
                         pm_help=None)

    def run(self):
        super().run(self.token)

    async def on_ready(self):
        for ext in self.startup_cogs:
            try:
                self.load_extension(f'cogs.{ext}')
            except:
                print(f'Failed to load {ext}.')
                traceback.print_exc()
            else:
                print(f'Loaded extension: {ext}.', end='\r')

        print(f'Client {self.user.name} logged in at {self.start_time}.')
        print('--------------------------------------------------------')
