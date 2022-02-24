import discord
import random

from GlobalVar import lista
from discord.ext import commands, tasks

class Status(commands.Cog):

    def __init__(self, client):
        self.client = client

    @tasks.loop(seconds=10800)
    async def change_status(self):
      randlista = random.choice(lista)
      await self.client.change_presence(activity=discord.Game(name = randlista))
        
    @commands.Cog.listener()
    async def on_ready(self):
        await self.client.wait_until_ready()
        self.change_status.start()

def setup(client):
    client.add_cog(Status(client))