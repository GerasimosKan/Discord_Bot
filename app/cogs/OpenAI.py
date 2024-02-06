import discord
from discord.ext import commands
from openai import APIConnectionError, OpenAI


class OpenAICog(commands.Cog):
    def __init__(self, bot, api_key):
        self.bot = bot
        # Initialize the OpenAI client with the provided API key
        self.openai_client = OpenAI(api_key=api_key)

    @commands.Cog.listener()
    async def on_message(self, message):
        # Ignore messages from the bot itself
        if message.author == self.bot.user:
            return

        # Check if the bot is mentioned in the message
        if self.bot.user.mentioned_in(message):
            # Extract the user's message (without the bot mention)
            user_input = message.content.replace(f"<@!{self.bot.user.id}>", "").strip()

            # Check if the user is trying to access the API command
            if user_input.lower().startswith("api"):
                try:
                    # Call OpenAI API to generate a response
                    chat_completion = await self.openai_client.chat.completions.create(
                        messages=[
                            {
                                "role": "user",
                                "content": user_input,
                            }
                        ],
                        model="gpt-3.5-turbo",
                    )
                    # Extract the response from the completion
                    response = chat_completion.choices[0].message.content
                    # Send the response back to the Discord channel
                    await message.channel.send(response)
                except APIConnectionError:
                    # Handle the case where there's an issue with the API connection
                    await message.channel.send(
                        "Sorry, there was an issue with the server. Please try again later."
                    )
            else:
                # Send a message to the user explaining to them that there's an issue with the API connection
                await message.channel.send(
                    f"{message.author.mention}, Sorry, there was an issue with the api :satellite:. Please try again later."
                )


def setup(bot):
    # OpenAI API key here
    api_key = "API-KEY"
    bot.add_cog(OpenAICog(bot, api_key))
