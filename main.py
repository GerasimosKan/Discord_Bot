import os
import discord

from os import system
from subprocess import call
from discord.utils import get
from private.config import TOKEN
from discord.ext import commands

intents = discord.Intents().all()
#intents = discord.Intents.default()
intents.typing = False
intents.members = True
intents.presences = False


bot = commands.Bot(command_prefix='!', intents=intents)
bot.remove_command('help')

# """ --- COGS HANDLING --- """


@bot.command
async def load(ctx, extension):
    bot.load_extension(f'cogs.{extension}')


@bot.command
async def unload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

# """ --- END COGS HANDLING --- """

# BOOT READY MESSAGE


@bot.event
async def on_ready():
    ListOfCogs = bot.cogs
    print(len(ListOfCogs))
    for NameOfCog, TheClassOfCog in ListOfCogs.items():
        print(NameOfCog)
    print(f'I have logged in as {bot.user}')


bot.run(TOKEN)
