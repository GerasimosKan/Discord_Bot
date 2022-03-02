from cgitb import text
import discord
import asyncio

from PIL import Image
from io import BytesIO
from PIL import ImageFont
from PIL import ImageDraw
from discord.ext import commands
from discord.ext.commands import Bot

class MemeGen(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

#MyID Command
    @commands.command(aliases=['id', 'ID'])
    async def MyID(self, ctx):

        img = Image.open('Discord_Bot/images/id.jpg') #image

        #draw = ImageDraw.Draw(img)
        #text= 
        #draw.text((356,112), text, (0, 0, 0,))
        
        author = ctx.message.author
        pfpi = author.avatar_url_as

        asset = pfpi(size=512)
        data = BytesIO(await asset.read())
        pfp = Image.open(data)

        pfp = pfp.resize((178,180)) #border size
        img.paste(pfp, (119,63)) #image paste location

        img.save("MyID.jpg")

        await ctx.send(file = discord.File("MyID.jpg"))

def setup(bot):
    bot.add_cog(MemeGen(bot))