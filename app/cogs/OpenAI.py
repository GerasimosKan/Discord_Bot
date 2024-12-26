import aiohttp
import discord
from discord.ext import commands


class AI(commands.Cog):
    def __init__(self, bot, server_url):
        self.bot = bot
        self.server_url = server_url

    @commands.command(
        name="- @ΕΛ.ΑΣ <message> -!",
        help="To use the AI, mention me and start your message.\nFor example: `@ΕΛ.ΑΣ coin flip` ",
    )
    async def openai_command(self, ctx):
        pass  # This function does nothing, it's just used to define the command

    @openai_command.error
    async def openai_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            # Ignore command not found errors
            return

        # Handle other errors
        await ctx.send("An error occurred while processing your request.")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        if self.bot.user.mentioned_in(message):
            user_input = message.content.replace(f"<@!{self.bot.user.id}>", "").strip()

            async with aiohttp.ClientSession() as session:
                try:
                    async with session.post(
                        f"{self.server_url}/api/generate",
                        json={"prompt": user_input, "model": "default"},
                    ) as response:
                        if response.status == 200:
                            data = await response.json()
                            response_text = data.get(
                                "response", "No response received from server."
                            )
                            await message.channel.send(response_text)
                        else:
                            await message.channel.send(
                                f"Sorry, there was an issue with the server (status code: {response.status}). Please try again later."
                            )
                except aiohttp.ClientError as e:
                    await message.channel.send(
                        f"Sorry, there was a connection issue: {str(e)}. Please try again later."
                    )


def setup(bot):
    server_url = "http://server.kanellatos.gr"
    bot.add_cog(AI(bot, server_url))
