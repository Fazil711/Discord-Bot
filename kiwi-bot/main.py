from discord.ext import commands
import os

bot = commands.Bot(command_prefix='$')
bot.remove_command('help')

cogs = ['cogs.mods'] 

for cogs in cogs:
  try:
    bot.load_extension(cogs)
  except Exception as e:
    raise e

bot.run('TOKEN')
