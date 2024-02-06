import discord
from discord.ext import commands


class CustomHelp(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def send_embed(self, ctx, embed):
        try:
            await ctx.send(embed=embed)
        except discord.Forbidden:
            await ctx.author.send(
                f"Hey, seems like I can't send any message in {ctx.channel.name} on {ctx.guild.name}\n"
                f"May you inform the server team about this issue? :slight_smile: ",
                embed=embed,
            )

    @commands.command(name="help", help="Display information about available commands.")
    async def custom_help(self, ctx, *args):
        prefix = "!"  # Change this to your command prefix

        if not args:
            emb = discord.Embed(
                title="Command Help",
                description=f"Use `{prefix}help <command>` for more details on a specific command.",
                color=discord.Color.blue(),
            )

            cogs_desc = ""
            for cog in self.bot.cogs:
                cogs_commands = [
                    command
                    for command in self.bot.get_cog(cog).get_commands()
                    if not command.hidden
                ]

                if cogs_commands:
                    cogs_desc += f"**{cog} Commands:**\n"
                    for command in cogs_commands:
                        cogs_desc += f"`{prefix}{command.name}` - {command.help}\n"
                    cogs_desc += "\n"

            emb.add_field(name="Available Commands", value=cogs_desc, inline=False)

        elif len(args) == 1:
            command = self.bot.get_command(args[0])
            if command:
                emb = discord.Embed(
                    title=f"Help for {command.name}",
                    description=command.help,
                    color=discord.Color.green(),
                )
                emb.add_field(
                    name="Usage", value=f"`{prefix}{command.name} {command.signature}`"
                )
                if command.aliases:
                    emb.add_field(
                        name="Aliases",
                        value=", ".join(f"`{alias}`" for alias in command.aliases),
                    )
            else:
                emb = discord.Embed(
                    title="Command Not Found",
                    description=f"No command named `{args[0]}` found.",
                    color=discord.Color.red(),
                )
        else:
            emb = discord.Embed(
                title="Invalid Command",
                description="Please provide a valid command for help.",
                color=discord.Color.orange(),
            )

        await self.send_embed(ctx, emb)


def setup(bot):
    bot.add_cog(CustomHelp(bot))
