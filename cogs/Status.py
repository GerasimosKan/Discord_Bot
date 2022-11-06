import discord
import random

from GlobalVar import lista
from discord.ext import commands, tasks


class Status(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @tasks.loop(seconds=10800)
    async def change_status(self):
        randlista = random.choice(lista)
        await self.bot.change_presence(activity=discord.Game(name=randlista))

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.wait_until_ready()
        self.change_status.start()


async def setup(bot):
    await bot.add_cog(Status(bot))
