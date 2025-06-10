from typing import Optional
from discord import Member, VoiceState
from discord.ext import commands, tasks
from datetime import datetime, timedelta

class AutoAFK(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.afk_timeout = 5  # minutes
        self.muted_users: dict[int, datetime] = {}
        self.afk_check.start()

    def cog_unload(self):
        self.afk_check.cancel()

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: Member, before: VoiceState, after: VoiceState):
        # Ignore bots or no channel change
        if member.bot or before.channel == after.channel:
            return
        
        afk_channel = member.guild.afk_channel
        if not afk_channel:
            return
        
        # User muted themselves
        if after.self_mute and not before.self_mute:
            self.muted_users[member.id] = datetime.utcnow()
        # User unmutes
        elif member.id in self.muted_users and not after.self_mute:
            self.muted_users.pop(member.id)

    @tasks.loop(minutes=1)
    async def afk_check(self):
        now = datetime.utcnow()
        threshold = timedelta(minutes=self.afk_timeout)
        
        for guild in self.bot.guilds:
            afk_channel = guild.afk_channel
            if not afk_channel:
                continue
            
            to_remove = []
            for user_id, muted_time in self.muted_users.items():
                if now - muted_time < threshold:
                    continue

                member = guild.get_member(user_id)
                if member and member.voice and member.voice.channel != afk_channel:
                    await member.move_to(afk_channel)
                    if guild.system_channel:
                        await guild.system_channel.send(
                            f"{member.mention} was moved to AFK for being muted over {self.afk_timeout} minutes."
                        )
                to_remove.append(user_id)
            
            for uid in to_remove:
                self.muted_users.pop(uid, None)

    @commands.command(name="set_afk_timeout")
    @commands.has_permissions(administrator=True)
    async def set_timeout(self, ctx: commands.Context, minutes: int):
        if minutes < 1:
            return await ctx.send("Timeout must be at least 1 minute.")
        self.afk_timeout = minutes
        await ctx.send(f"AFK timeout set to **{minutes}** minutes for self-muted users.")

async def setup(bot: commands.Bot):
    await bot.add_cog(AutoAFK(bot))
