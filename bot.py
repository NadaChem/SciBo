import json
import traceback 

from datetime import datetime
from discord.ext import commands


class SciBo(commands.Bot):
    def __init__(self):
        self.description = 'A scientific bot that does science-y things'
        self.start_time = datetime.now()
        self.startup_cogs = ['trivia']
        with open('data/keys.json') as f:
            self.token = json.load(f)['discord']

        super().__init__(command_prefix='sci>', description=self.description, pm_help=None)

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
