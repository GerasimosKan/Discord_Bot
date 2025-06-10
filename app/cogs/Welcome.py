from io import BytesIO
import discord
from discord.ext import commands
from PIL import Image
import aiohttp

Channel_ID = 546662624243220494
Role_ID = 546665144822923265

class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        try:
            # Get channel and role
            channel = self.bot.get_channel(Channel_ID)
            role = discord.utils.get(member.guild.roles, id=Role_ID)

            if not channel or not role:
                print("Channel or role not found.")
                return

            # Load base image
            img = Image.open("./images/id.jpg")
            
            # Get avatar URL (with fallback to default avatar)
            avatar_url = str(member.avatar.url) if member.avatar else str(member.default_avatar.url)
            
            # Download avatar using aiohttp
            async with aiohttp.ClientSession() as session:
                async with session.get(avatar_url) as resp:
                    if resp.status != 200:
                        print(f"Failed to download avatar for {member.display_name}")
                        return
                    avatar_data = await resp.read()
            
            # Process the image
            pfp = Image.open(BytesIO(avatar_data))
            pfp = pfp.resize((178, 180))
            img.paste(pfp, (119, 63))

            # Save and send the image
            with BytesIO() as image_binary:
                img.save(image_binary, "JPEG", quality=85)
                image_binary.seek(0)
                await channel.send(
                    f"Welcome, {member.mention}, here is your new ID!",
                    file=discord.File(image_binary, filename="MyID.jpg"),
                )

            # Add welcome role
            await member.add_roles(role)
            
        except discord.Forbidden:
            print(f"Missing permissions to welcome {member.display_name}")
        except discord.HTTPException as e:
            print(f"Discord API error during welcome: {e}")
        except Exception as e:
            print(f"Unexpected error in on_member_join: {type(e).__name__} - {e}")

async def setup(bot):
    await bot.add_cog(Welcome(bot))