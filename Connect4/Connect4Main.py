from discord.ext import commands
from Connect4App import connect4Main

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print("Bot is online")

@bot.command(pass_context = True)
async def Connect4(ctx):
    await connect4Main(ctx, bot)


bot.run('token') #Invalid token set for uploaded code, use your own discord bot's token to run this code on it