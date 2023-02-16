import os
import discord
from discord.ext import commands
from gtts import gTTS
import time
import asyncio
from keep_alive import keep_alive

keep_alive()

token = os.environ['token']
bot = commands.Bot(command_prefix='!',
                   activity=None,
                   status=discord.Status.idle,
                   intents=discord.Intents.all())


@bot.event
async def on_ready():
    print('logged in as {0.user}'.format(bot))
    discord.opus.load_opus("./libopus.so.0.8.0")


@bot.command()
async def test(ctx):
    print("ok")


@bot.command()
async def boogoo(ctx):
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    stopped = False
    await bot.change_presence(activity=discord.Game(name="BooGoo"))
    channel = ctx.author.voice.channel
    print("boogoo!")
    now = time.gmtime()
    interval = 1
    if now[4] % interval == 0 and now[5] == 0:
        v = await channel.connect()
        vc = ctx.guild.voice_client
        print(vc)
        txt = "現在是" + str((now[3] + 8) % 24) + "點" + str(now[4]) + "分"
        tts = gTTS(txt, lang='zh')
        fn = 'boogoo.mp3'
        tts.save(fn)
        v.play(discord.FFmpegPCMAudio(fn))
        time.sleep(5)
        await vc.disconnect()

    while not stopped:
        try:
            message = await bot.wait_for("message", check=check, timeout=0.8)
            stopped = True if message.content.lower() == "!stop" else False
        except asyncio.TimeoutError:
            now = time.gmtime()
            interval = 5
            if now[4] % interval == 0 and now[5] == 0:
                v = await channel.connect()
                vc = ctx.guild.voice_client
                print(vc)
                txt = "現在是" + str((now[3] + 8) % 24) + "點" + str(now[4]) + "分"
                tts = gTTS(txt, lang='zh')
                fn = 'boogoo.mp3'
                tts.save(fn)
                v.play(discord.FFmpegPCMAudio(fn))
                time.sleep(5)
                await vc.disconnect()
    if stopped:
        print("stopped")
        await bot.change_presence(status=discord.Status.idle)
        return


try:
    bot.run(token)
except discord.HTTPException as e:
    if e.status == 429:
        print(
            "The Discord servers denied the connection for making too many requests"
        )
        print(
            "Get help from https://stackoverflow.com/questions/66724687/in-discord-py-how-to-solve-the-error-for-toomanyrequests"
        )
    else:
        raise e
