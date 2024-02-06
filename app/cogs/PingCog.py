from discord.ext import commands


class PingPong(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ping", help="Check the bot's latency.")
    async def ping_command(self, ctx):
        # Mention the user who issued the command
        user_mention = ctx.author.mention

        # Get the bot's latency to the server
        bot_latency = round(ctx.bot.latency * 1000)  # Convert to milliseconds

        # Send a message with "Pong!", the user mention, and the bot's latency
        await ctx.send(
            f"Pong! {user_mention} :ping_pong: Bot latency: {bot_latency} ms"
        )


def setup(bot):
    bot.add_cog(PingPong(bot))
