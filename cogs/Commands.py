import discord
import asyncio

from PIL import Image
from io import BytesIO
from cgitb import text
from PIL import ImageFont
from PIL import ImageDraw
from discord.ext import commands
from discord.ext.commands import Bot



class Commands(commands.Cog):

    """List of custom commands"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["purge", "delete", "cl"], title="Purge", description=f"Purges channels messages")
    async def clear(self, ctx, ammount=13):
        """Purges channel messages"""

        if(not ctx.author.guild_permissions.manage_messages):
            await ctx.send("Ato einai paronomo :octagonal_sign:")
            return

        ammount= ammount+1

        if ammount >14:
            await ctx.send("Mexri 13 minimata blaka :mountain:")
        else:
            await ctx.channel.purge(limit=ammount)
            await ctx.send("Katharisa bouno mou! :mountain:")



#MyID Command
    @commands.command(aliases=['id', 'ID'])
    async def MyID(self, ctx):
        """Blepeis tin tautotita sou"""

        img = Image.open('/home/pi/Discord_Bot/images/id.jpg') #image

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
    bot.add_cog(Commands(bot))
