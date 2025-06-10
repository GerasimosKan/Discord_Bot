from discord.ext import commands

class PingPong(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ping", help="Check the bot's latency.")
    async def ping_command(self, ctx):
        user_mention = ctx.author.mention
        bot_latency = round(ctx.bot.latency * 1000)
        await ctx.send(f"Pong! {user_mention} :ping_pong: Bot latency: {bot_latency} ms")

async def setup(bot):
    await bot.add_cog(PingPong(bot))