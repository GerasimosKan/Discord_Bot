import discord
from discord.ext import commands
from openai import APIConnectionError, OpenAI


class AI(commands.Cog):
    def __init__(self, bot, api_key):
        self.bot = bot
        self.openai_client = OpenAI(api_key=api_key)

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

            if user_input.lower().startswith("api"):
                try:
                    chat_completion = await self.openai_client.chat.completions.create(
                        messages=[
                            {
                                "role": "user",
                                "content": user_input,
                            }
                        ],
                        model="gpt-3.5-turbo",
                    )
                    response = chat_completion.choices[0].message.content
                    await message.channel.send(response)
                except APIConnectionError:
                    await message.channel.send(
                        "Sorry, there was an issue with the server. Please try again later."
                    )
            else:
                await message.channel.send(
                    f"{message.author.mention}, Sorry, there was an issue with the api :satellite:. Please try again later."
                )


def setup(bot):
    api_key = "API-KEY"
    bot.add_cog(AI(bot, api_key))
