import spacy, requests
from pathlib import Path
import discord
from discord.ext import commands, tasks




intents = discord.Intents.default()
intents.members = True

BOT_PREFIX = ('trauma ')
bot = commands.Bot(command_prefix=BOT_PREFIX, intents = intents)

@bot.event
async def on_ready():
	print (f"\nLogged in as:\t {str(bot.user)}")
	print ("-----------------")
	change_presence.start()

@tasks.loop(seconds = 3600)
async def change_presence():
	await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="sudo help"))

@bot.event
async def on_command_error(ctx, error):
	if isinstance(error, commands.CommandNotFound):
		embed = discord.Embed(description=f"○ Invalid command\n○ Type `trauma help` to know about each command.",colour=discord.Colour.red())
		await ctx.send(embed = embed)
		return


if __name__ == '__main__':
	res = Path("res")
	with open(res / "discord_token", 'r') as TokenObj:
		DISCORD_TOKEN = TokenObj.read()

	cogs = [
		'cogs.features.ask',
		]
	for cog in cogs:
		print ("Loading Cog:\t", cog, "...")
		bot.load_extension(cog)

	bot.run(DISCORD_TOKEN)