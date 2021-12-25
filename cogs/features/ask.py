import discord
from discord.ext import commands
import requests
from pathlib import Path 
import spacy



nlp = spacy.load("en_core_web_md")
def get_weather(city):
	res = Path("res")
	with open(res / "openweather", 'r') as TokenObj:
		OW_TOKEN = TokenObj.read()
	api_url = "http://api.openweathermap.org/data/2.5/weather?q={}&appid={}".format(city, OW_TOKEN)
	weather_json = requests.get(api_url).json()
	print(weather_json["weather"])
	weather = weather_json["weather"][0]["description"]
	return weather


def chatbot(statement):
	weather = nlp("Current weather in a city")
	statement = nlp(statement)
	min_similarity = 0.75

	if weather.similarity(statement) >= min_similarity:
		for ent in statement.ents:
			if ent.label_ == "GPE": # GeoPolitical Entity
				city = ent.text
				break
			else:
				return "You need to tell me a city to check."

		city_weather = get_weather(city)
		if city_weather is not None:
			return "In " + city + ", the current weather is: " + city_weather
		else:
			return "Something went wrong."
	else:
		return "Sorry I don't understand that. Please rephrase your statement."

res = Path("res")
with open(res / "openweather", 'r') as TokenObj:
	OW_TOKEN = TokenObj.read()

class src(commands.Cog):
	
	def __init__(self,bot):
		self.bot = bot

	@commands.command(help = "where is trauma  | trauma where")
	async def where(self,ctx) :
		gitembed= discord.Embed(title='')

		gitembed.add_field(name='Trauma',value="I am here",inline=True)
	
		await ctx.send(embed=gitembed)

	@commands.command(help = "nothing | trauma sup")
	async def sup(self,ctx) :
		gitembed= discord.Embed(title='')

		gitembed.add_field(name='Trauma',value="Just trying to make a bot before discord.py goes extinct",inline=True)
	
		await ctx.send(embed=gitembed)

	@commands.command(help = "tells weather in a city | trauma weather <city>")
	async def weather(self, ctx, *city):
		print(city[0])
		res = Path("res")
		with open(res / "openweather", 'r') as TokenObj:
			OW_TOKEN = TokenObj.read()
		api_url = "http://api.openweathermap.org/data/2.5/weather?q={}&appid={}".format(city[0], OW_TOKEN)
		weather_json = requests.get(api_url).json()
		weather = weather_json["weather"][0]["description"]
		print(weather)
		await ctx.send(weather)

	@commands.command(help = "talk to trauma | trauma ask <statement>")
	async def ask(self, ctx, *statement):
		print(chatbot(" ".join(statement[0:])))
		await ctx.send(chatbot(" ".join(statement[0:])))

	@commands.command(help = "Gives Source | trauma src")
	async def src(self, ctx, *statement):
		embed= discord.Embed(title='')
		embed.add_field(name='Github HTTPS Source',value="https://github.com/siddarthreddygsr/Traumatic-Weather-bot.git",inline=True)
		embed.add_field(name='Github SSH Source',value="git@github.com:siddarthreddygsr/Traumatic-Weather-bot.git",inline=True)
		await ctx.send(embed=embed)
		
def setup(bot):
	bot.add_cog(src(bot))