import discord
from discord.ext import commands


class RespondLogic(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):

        if message.content == "test":
            await message.channel.send(f"{message.author.mention} Test Succes")
        

def setup(bot):
    bot.add_cog(RespondLogic(bot))
