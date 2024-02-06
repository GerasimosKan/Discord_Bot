import os

import discord
from discord.ext import commands

# Create the bot instance with a command prefix
intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)
bot.remove_command("help")

# Automatically load all cogs from the 'cogs' directory
for filename in os.listdir("app/cogs"):
    if filename.endswith(".py"):
        cog_name = f"cogs.{filename[:-3]}"
        try:
            # Load each cog using load_extension
            bot.load_extension(cog_name)

        except Exception as e:
            print(f"Failed to load cog {cog_name}: {e}")


@bot.event
async def on_ready():
    # Get a list of loaded cogs
    loaded_cogs = [cog for cog in bot.cogs]

    # Print the number of loaded cogs
    print(f"Number of loaded cogs: {len(loaded_cogs)}")

    # Print the names of loaded cogs
    for index, cog_name in enumerate(loaded_cogs, 1):
        print(f"{index}. {cog_name}")

    # Print bot information when it is ready
    print(f"Logged in as {bot.user.name} ({bot.user.id})")


# Run the bot with the specified token
bot_token = "Token"
bot.run(bot_token)
