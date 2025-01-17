import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')

@bot.command()
async def ping(ctx):
    await ctx.send(f'Pong! Latency: {round(bot.latency * 1000)}ms')

bot.run('MTMwNzA1Mjg4ODM1MDEzMDE3Ng.GJYdu3.FwSwil5fkeqYiXUi3FmXxBTxM0L55tQz4OLnVo')