import discord
from discord.ext import commands

TOKEN = "YOUR_BOT_TOKEN"
PREFIX = "!"

bot = commands.Bot(command_prefix=PREFIX)

@bot.event
async def on_ready():
    print("Ready")

@bot.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(bot.latency, 1)}')

bot.run(TOKEN)
