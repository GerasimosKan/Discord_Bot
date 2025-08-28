import os
import sys
import traceback
import discord
from discord.ext import commands
import asyncio
from dotenv import load_dotenv

load_dotenv()

class MyBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.members = True
        intents.message_content = True
        super().__init__(command_prefix="!", intents=intents, help_command=None)

    async def setup_hook(self):
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py"):
                ext = f"cogs.{filename[:-3]}"
                try:
                    await self.load_extension(ext)
                    print(f"✅ Loaded cog: {ext}")
                except Exception as e:
                    print(f"❌ Failed to load {ext}: {e}")

    async def on_ready(self):
        print(f"🚀 Logged in as {self.user} (ID: {self.user.id})")
        print("🔌 Loaded cogs:")
        for i, name in enumerate(self.cogs, start=1):
            print(f"  {i}. {name}")

    async def on_command_error(self, ctx: commands.Context, error: commands.CommandError):
        # Unwrap errors from command invocation
        if isinstance(error, commands.CommandInvokeError):
            original = error.original
        else:
            original = error

        # Handle common command errors
        if isinstance(original, commands.CommandNotFound):
            return  # ignore unknown commands
        elif isinstance(original, commands.MissingRequiredArgument):
            await ctx.send(f"❗ Missing argument: `{original.param.name}`")
        elif isinstance(original, commands.BadArgument):
            await ctx.send("❗ Bad argument provided.")
        elif isinstance(original, commands.MissingPermissions):
            await ctx.send("❌ You don't have permissions for that command.")
        elif isinstance(original, commands.BotMissingPermissions):
            await ctx.send("❌ I lack the required permissions to run that command.")
        elif isinstance(original, commands.CommandOnCooldown):
            await ctx.send(f"⏳ This command is on cooldown. Try again in {original.retry_after:.2f}s.")
        else:
            # Log unexpected errors
            print(f"Ignoring exception in command {ctx.command}:", file=sys.stderr)
            traceback.print_exception(type(original), original, original.__traceback__, file=sys.stderr)
            await ctx.send("⚠️ An unexpected error occurred. Check logs for details.")

async def main():
    bot = MyBot()
    print("🔥 Starting bot...")
    token = os.getenv("DISCORD_TOKEN")
    async with bot:
        await bot.start(token)
if __name__ == "__main__":
    asyncio.run(main())
