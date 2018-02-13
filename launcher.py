#!/bin/env python3

from bot import SciBo


if __name__ == '__main__':
    bot = SciBo()
    bot.remove_command('help')
    bot.run()
