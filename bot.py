import discord
from discord.ext import commands
import yt_dlp

TOKEN = "MTUxMDE1OTkzNjQyNzEzMDk1MA.G1HGdf.xR8B3ylpKs14zy4v_7aoW8AIeg--Z7QrBiV8wU"

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

ydl_opts = {
    "format": "bestaudio/best",
    "quiet": True,
    "noplaylist": True
}


def play_loop(vc, audio_url):
    source = discord.FFmpegPCMAudio(
        audio_url,
        executable="ffmpeg"
    )

    vc.play(
        source,
        after=lambda e: play_loop(vc, audio_url) if not e and vc.is_connected() else None
    )


@bot.command()
async def play(ctx, url):
    if not ctx.author.voice:
        return await ctx.send("Əvvəl səs kanalına qoşul.")

    channel = ctx.author.voice.channel

    if ctx.voice_client is None:
        vc = await channel.connect()
    else:
        vc = ctx.voice_client

    if vc.is_playing():
        vc.stop()

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

            if "entries" in info:
                info = info["entries"][0]

            audio_url = info["url"]
            title = info.get("title", "Naməlum")

        play_loop(vc, audio_url)

        await ctx.send(f"🔁 Təkrarda çalınır: **{title}**")

    except Exception as e:
        await ctx.send(f"Xəta: {e}")


@bot.command()
async def stop(ctx):
    vc = ctx.voice_client

    if vc:
        vc.stop()
        await vc.disconnect()
        await ctx.send("⏹ Dayandırıldı.")


bot.run(TOKEN)
