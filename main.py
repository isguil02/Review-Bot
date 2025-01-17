import dotenv
import os
import discord
from discord.ext import commands, tasks
import asyncio
import sqlite3
import math

dotenv.load_dotenv()
bot = commands.Bot(command_prefix='.',intents=discord.Intents.all())


@bot.event
async def on_ready():
    try: 
        synced_commands = await bot.tree.sync()
        print(f"Synced {len(synced_commands)} commands.")
    except Exception as e:
        print("An error ocured with syncing",e)

@bot.command()
async def test(ctx):
    print("yo")
    await ctx.send(f"hi\nhru")

async def Load():    
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")

async def main():
    async with bot:
        await Load()
        await bot.start(os.getenv('TOKEN'))


asyncio.run(main())

