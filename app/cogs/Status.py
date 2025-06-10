import random
import discord
from discord.ext import commands, tasks

lista = [
    "Μαινόμενη άβυσσος",
    "Με κάτι γύφτους",
    "Ουράνιο τόξο 6 | Πολιορκία",
    "Φαράγγι Των Επικαλεστών",
    "Grand Theft Auto: San Andreas",
    "Counter-Strike: Global Offensive » Inferno",
]

class Status(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @tasks.loop(seconds=10800)
    async def change_status(self):
        randlista = random.choice(lista)
        await self.bot.change_presence(activity=discord.Game(name=randlista))

    @commands.Cog.listener()
    async def on_ready(self):
        self.change_status.start()

async def setup(bot):
    await bot.add_cog(Status(bot))