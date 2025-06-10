import discord
from discord.ext import commands
import yt_dlp
import asyncio

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.queues = {}

    def get_queue(self, guild_id):
        return self.queues.setdefault(guild_id, [])

    def search_youtube(self, query):
        ydl_opts = {
            "format": "bestaudio/best",
            "noplaylist": True,
            "default_search": "ytsearch",
            "quiet": True,
            "ignoreerrors": True,
            "skip_download": True,
            "flat_playlist": True,
            "cookiefile": "./data/cookies.txt", 
            "extractor_args": {}
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                info = ydl.extract_info(query, download=False)
                if "entries" in info:
                    info = info["entries"][0]
                return {"url": info["url"], "title": info["title"]}
            except Exception as e:
                print(f"Error searching YouTube: {e}")
                return None

    async def play_next(self, ctx):
        queue = self.get_queue(ctx.guild.id)
        if not queue:
            return

        song = queue.pop(0)
        ffmpeg_opts = {
            "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
            "options": "-vn -c:a libopus -b:a 420k"
        }

        try:
            source = await discord.FFmpegOpusAudio.from_probe(song["url"], **ffmpeg_opts)
            vc = ctx.voice_client
            vc.play(
                source,
                after=lambda e: asyncio.run_coroutine_threadsafe(self.play_next(ctx), self.bot.loop)
            )
            await ctx.send(f"🎶 Now playing: **{song['title']}**")
        except Exception as e:
            await ctx.send("⚠️ Error playing the song.")
            print(f"Playback error: {e}")

    @commands.command(
        aliases=["p"],
        help="Play or Search a song.",
        description="Searches YouTube and plays the best audio quality in the voice channel."
    )
    async def play(self, ctx, *, query):
        """Play a song from YouTube"""
        if not ctx.author.voice:
            return await ctx.send("❌ You must be in a voice channel.")
        if ctx.voice_client is None:
            await ctx.author.voice.channel.connect()

        song = self.search_youtube(query)
        if not song:
            return await ctx.send("❌ Couldn't find the song.")

        queue = self.get_queue(ctx.guild.id)
        queue.append(song)

        if not ctx.voice_client.is_playing():
            await self.play_next(ctx)
        else:
            await ctx.send(f"📥 Queued: **{song['title']}**")

    @commands.command(
        aliases=["s", "next"],
        help="Skip the current song.",
        description="Stops the current song and plays the next one in the queue."
    )
    async def skip(self, ctx):
        """Skip the current song."""
        if ctx.voice_client and ctx.voice_client.is_playing():
            ctx.voice_client.stop()
            await ctx.send("⏭️ Skipped.")
        else:
            await ctx.send("⚠️ Nothing is playing.")

    @commands.command(
        aliases=["clear", "end"],
        help="Stop playing and clear the queue.",
        description="Immediately stops playback and removes all queued songs."
    )
    async def stop(self, ctx):
        """Stop playback and clear the queue."""
        if ctx.voice_client:
            self.queues[ctx.guild.id] = []
            ctx.voice_client.stop()
            await ctx.send("⏹️ Stopped and cleared queue.")

    @commands.command(
        aliases=["dc", "disconnect", "bye"],
        help="Disconnect the bot from the voice channel.",
        description="Forces the bot to leave the current voice channel."
    )
    async def leave(self, ctx):
        """Disconnect the bot from the voice channel."""
        if ctx.voice_client:
            await ctx.voice_client.disconnect()
            await ctx.send("👋 Left the voice channel.")
        else:
            await ctx.send("❌ Not in a voice channel.")

async def setup(bot):
    await bot.add_cog(Music(bot))
