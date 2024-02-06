import asyncio
import os
from io import BytesIO

import discord
from discord.ext import commands
from PIL import Image


class Commands(commands.Cog):
    """List of custom commands"""

    def __init__(self, bot):
        self.bot = bot

    # Purge Command
    @commands.command(
        aliases=["delete", "del"],
        title="Purge",
        description=f"Purges channels messages",
    )
    async def purge(self, ctx, amount=13):
        """Purges channel messages"""
        try:
            # Check if the user has the necessary permissions
            if not ctx.author.guild_permissions.manage_messages:
                await ctx.send(
                    f":no_entry_sign: {ctx.author.mention}, you do not have the necessary permissions to use this command."
                )
                return

            # Ensure amount is between 1 and 14
            amount = min(amount + 1, 14)

            # Add a delay before purging to avoid issues
            await asyncio.sleep(1)

            # Purge messages, including the command message
            deleted_messages = await ctx.channel.purge(limit=amount)

            # Send a response after purging
            response_message = await ctx.send(
                f":white_check_mark: {ctx.author.mention}, successfully purged {len(deleted_messages)} messages! :wastebasket:"
            )

            # Notify if more than 13 messages were deleted
            if len(deleted_messages) > 13:
                await ctx.send(
                    f":information_source: Cleared {len(deleted_messages)} messages in {ctx.channel.mention}! :wastebasket:"
                )

            # Delete the command and response messages if they exist
            try:
                await ctx.message.delete()
                await response_message.delete()
            except discord.NotFound:
                pass  # Messages already deleted or not found

        except Exception as e:
            print(f"Error in purge command: {type(e).__name__} - {e}")

    # MyID Command
    @commands.command(aliases=["id", "ID"])
    async def my_id(self, ctx):
        """Blepeis tin tautotita sou"""
        try:
            # Load base image
            img = Image.open("app/images/id.jpg")

            # Open user's avatar as an image
            author = ctx.message.author
            pfp_url = author.avatar_url_as(size=512)
            pfp = Image.open(BytesIO(await pfp_url.read()))

            # Resize and paste user's avatar onto the base image
            pfp = pfp.resize((178, 180))
            img.paste(pfp, (119, 63))

            # Save the processed image
            img.save("MyID.jpg")

            # Send the processed image
            await ctx.send(file=discord.File("MyID.jpg"))
        except Exception as e:
            await ctx.send(f"An error occurred: {type(e).__name__} - {e}")

    # Ptixio Command
    @commands.command(aliases=["paper", "ptixio"])
    async def certificate(self, ctx):
        """Ptixio"""
        try:
            # Load base image
            img = Image.open("app/images/paper.png")

            # Open user's avatar as an image
            author = ctx.message.author
            pfp_url = author.avatar_url_as(size=512)
            pfp = Image.open(BytesIO(await pfp_url.read()))

            # Resize and paste user's avatar onto the base image
            pfp = pfp.resize((200, 200))
            img.paste(pfp, (430, 253))

            # Save and send the processed image
            img.save("paper.png")
            await ctx.send(file=discord.File("paper.png"))

            # Remove the saved image file
            os.remove("paper.png")
        except Exception as e:
            await ctx.send(f"An error occurred: {type(e).__name__} - {e}")

    async def cog_command_error(self, ctx, error):
        # Handle errors specific to this cog
        if isinstance(error, commands.CommandError):
            await ctx.send(f"Error: {error}")


def setup(bot):
    bot.add_cog(Commands(bot))
