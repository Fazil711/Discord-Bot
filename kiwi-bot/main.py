from discord.ext import commands
import os
#from keep_alive import keep_alive

bot = commands.Bot(command_prefix='$')
bot.remove_command('help')

cogs = ['cogs.mods', 'cogs.GoogleClass'] 

for cogs in cogs:
  try:
    bot.load_extension(cogs)
  except Exception as e:
    raise e


bot.run('Token')
