from io import BytesIO

import discord
from discord.ext import commands
from PIL import Image

Channel_ID = 546662624243220494
Role_ID = 546665144822923265


class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        try:
            # Get the channel and role using IDs
            channel = self.bot.get_channel(Channel_ID)
            role = discord.utils.get(member.guild.roles, id=Role_ID)

            # Ensure both the channel and role are valid
            if not channel or not role:
                print("Channel or role not found.")
                return

            img = Image.open("app/images/id.jpg")  # Open the base image
            asset = member.avatar_url_as(size=512)
            data = BytesIO(await asset.read())
            pfp = Image.open(data)

            pfp = pfp.resize((178, 180))  # Resize the profile picture
            img.paste(pfp, (119, 63))  # Paste the profile picture onto the base image

            # Save the processed image
            with BytesIO() as image_binary:
                img.save(image_binary, "JPEG")
                image_binary.seek(0)

                # Use an f-string to format the welcome message
                welcome_message = f"Welcome, {member.mention}, here is your new ID!"

                # Send the welcome message with the processed image
                await channel.send(
                    welcome_message,
                    file=discord.File(image_binary, filename="MyID.jpg"),
                )

            # Add the role to the new member
            await member.add_roles(role)
        except Exception as e:
            print(f"Error in on_member_join: {e}")


def setup(bot):
    bot.add_cog(Welcome(bot))
