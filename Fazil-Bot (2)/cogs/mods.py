import discord 
from discord.ext import commands
import requests
import random
import json
import asyncio
from responses import responses
from googlesearch import search
from discord.ext.commands.core import has_permissions


def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return (quote)
  
class Mods(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
  @commands.Cog.listener()
  async def on_ready(self):
    print("We have logged in as {0.user}".format(self.bot))
      

  @commands.Cog.listener()
  async def on_message(self, message):
    if message.author == self.bot.user:
      return 
    message.content = message.content.lower()
    if message.content.startswith('hello'):
      await message.channel.send("Hello!")
    if message.content.startswith('inspire'):
      quote = get_quote()
      await message.channel.send(quote)
    if message.content.startswith('cool'):
      await message.channel.send("cool cool cool")
    if message.content.startswith('Stackoverflow'):
      await message.channel.send("https://stackoverflow.com/")
    if message.content.startswith('just google'):
      searchContent = " "
      text = str(message.content).split(' ')
      for i in range(2, len(text)):
        searchContent = searchContent + text[i]
      for j in search(searchContent, tld = "co.in", num = 1, stop = 1, pause = 2):
        await message.channel.send(j)

  @commands.command()
  async def test(self, ctx, arg):
    await ctx.send(arg)

  @commands.command()
  async def kiwi(self, ctx, *, args):
    await ctx.send(random.choice(responses))

  @commands.command()
  @has_permissions(administrator = True)
  async def ban(self, ctx, member: discord.Member, *, reason=None):
          embed = discord.Embed(
              title="Banned",
              colour=0x2859B8,
              description=f"{member.mention} has been banned.",
          )
          await member.ban(reason=reason)
          await ctx.send(embed=embed)
  @ban.error
  async def ban_error(self, ctx, error):
      if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(
              title="Lol",
              colour=0x2859B8,
              description="You don't even have perms for that!",
        )
        await ctx.send(embed = embed)

  @commands.command()
  @has_permissions(administrator = True)
  async def kick(self, ctx, member: discord.Member, *, reason=None):
          embed = discord.Embed(
              title="Kicked",
              colour=0x2859B8,
              description=f"{member.mention} has been kicked.",
          )
          await member.kick(reason=reason)
          await ctx.send(embed=embed)
  @kick.error
  async def kick_error(self, ctx, error):
      if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(
              title="Lol",
              colour=0x2859B8,
              description="You don't even have perms for that!",
        )
        await ctx.send(embed = embed)

  @commands.command()
  @has_permissions(administrator = True)
  async def unban(self, ctx, *, member):
      banned_users = await ctx.guild.bans()

      member_name, member_discriminator = member.split('#')
      for ban_entry in banned_users:
          user = ban_entry.user

          if (user.name, user.discriminator) == (member_name, member_discriminator):
              await ctx.guild.unban(user)
              embed = discord.Embed(
              title="Unbanned",
              colour=0x2859B8,
              description=f"Unbanned: {user.mention}",
              )
              await ctx.channel.send(embed = embed)
              return
  @commands.command(pass_context = True)
  async def help(self, ctx):
    embed = discord.Embed(
      colour = discord.Colour.orange()
    )
    embed.set_author(name ='Help')
    embed.add_field(name = '$kiwi', value = 'Returns random answer', inline = False)
    embed.add_field(name = 'inspire', value = 'Returns inspirational quotes', inline = False)
    embed.add_field(name = 'Just Google', value = 'Returns googles first result', inline = False)
    embed.add_field(name = '$test', value = 'Returns exact same statement', inline = False)
    await ctx.send(embed = embed)

def setup(bot):
  bot.add_cog(Mods(bot))