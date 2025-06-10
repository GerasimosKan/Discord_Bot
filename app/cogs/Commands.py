import asyncio
import os
from io import BytesIO
import discord
from discord.ext import commands
from PIL import Image
import aiohttp


class Commands(commands.Cog):
    """List of custom commands"""

    def __init__(self, bot):
        self.bot = bot

    # Revoke Command
    @commands.command(title="Revoke", description=f"Revoke channels messages")
    async def revoke(self, ctx, limit: int):
        """Revokes a specified number of messages in the channel."""
        if not 1 <= limit <= 100:
            await ctx.send("Please provide a number between 1 and 100.")
            return

        try:
            await ctx.message.delete()
            deleted = await ctx.channel.purge(limit=limit)
            await ctx.send(f"Deleted {len(deleted)} message(s).", delete_after=5)
        except discord.Forbidden:
            await ctx.send("I do not have the permissions to delete messages.")
        except discord.HTTPException:
            await ctx.send("Failed to delete messages.")

    # Purge Command
    @commands.command(
        aliases=["delete", "del"],
        title="Purge",
        description="Purges channel messages"
    )
    async def purge(self, ctx, amount: int = 13):
        """Purges a specified number of messages, without exceeding the requested amount."""
        try:
            if not ctx.author.guild_permissions.manage_messages:
                await ctx.send(
                    f":no_entry_sign: {ctx.author.mention}, you do not have permission to use this command."
                )
                return

            if amount < 1:
                await ctx.send(":warning: Amount must be at least 1.")
                return
            amount = min(amount, 13)

            await asyncio.sleep(1)
            deleted_messages = await ctx.channel.purge(limit=amount + 1)

            confirmation_message = await ctx.send(
                f":white_check_mark: {ctx.author.mention}, successfully purged {len(deleted_messages) - 1} messages! :wastebasket:"
            )

            await asyncio.sleep(3)
            await confirmation_message.delete()

        except discord.DiscordException as e:
            await ctx.send(f":x: An error occurred: {str(e)}")
        except Exception as e:
            print(f"Error in purge command: {type(e).__name__} - {e}")

    # MyID Command
    @commands.command(aliases=["id", "ID"])
    async def my_id(self, ctx):
        """Blepeis tin tautotita sou"""
        try:
            img = Image.open("./images/id.jpg")
            author = ctx.message.author
            
            # Get avatar URL with fallback to default avatar
            avatar_url = str(author.avatar.url) if author.avatar else str(author.default_avatar.url)
            
            # Create a new session for this request
            async with aiohttp.ClientSession() as session:
                async with session.get(avatar_url) as resp:
                    if resp.status == 200:
                        pfp = Image.open(BytesIO(await resp.read()))
                    else:
                        await ctx.send("Failed to download avatar image.")
                        return

            pfp = pfp.resize((178, 180))
            img.paste(pfp, (119, 63))
            
            # Save to bytes instead of file
            with BytesIO() as image_binary:
                img.save(image_binary, 'JPEG')
                image_binary.seek(0)
                await ctx.send(file=discord.File(fp=image_binary, filename='MyID.jpg'))
                
        except Exception as e:
            await ctx.send(f"An error occurred: {type(e).__name__} - {e}")

    # Ptixio Command
    @commands.command(aliases=["paper", "ptixio"])
    async def certificate(self, ctx):
        """Ptixio"""
        try:
            img = Image.open("./images/paper.png")
            author = ctx.message.author
            
            # Get avatar URL with fallback to default avatar
            avatar_url = str(author.avatar.url) if author.avatar else str(author.default_avatar.url)
            
            # Create a new session for this request
            async with aiohttp.ClientSession() as session:
                async with session.get(avatar_url) as resp:
                    if resp.status == 200:
                        pfp = Image.open(BytesIO(await resp.read()))
                    else:
                        await ctx.send("Failed to download avatar image.")
                        return

            pfp = pfp.resize((200, 200))
            img.paste(pfp, (430, 253))
            
            # Save to bytes instead of file
            with BytesIO() as image_binary:
                img.save(image_binary, 'PNG')
                image_binary.seek(0)
                await ctx.send(file=discord.File(fp=image_binary, filename='paper.png'))
                
        except Exception as e:
            await ctx.send(f"An error occurred: {type(e).__name__} - {e}")

async def setup(bot):
    await bot.add_cog(Commands(bot))