import discord
from discord.ext import commands


class RespondLogic(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):

        if message.content == "gay":
            await message.channel.send(f"{message.author.mention} gamo tin mana sou")


async def setup(bot):
    await bot.add_cog(RespondLogic(bot))
