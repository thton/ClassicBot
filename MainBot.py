#Classic Bot
#Made by Toan Ton

import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
from itertools import cycle
import random

with open('botKey.txt', 'r') as key:
	botKey = key.readline()

classicBot = commands.Bot(command_prefix='#')
statuses = ["Growing Potatoes", "Code forever", "Azur Lane"]

async def change_status():
	await classicBot.wait_until_ready()
	status = cycle(statuses)
	while not classicBot.is_closed:
		current_status = next(status)
		await classicBot.change_presence(game=discord.Game(name=current_status))
		await asyncio.sleep(60)

@classicBot.event
async def on_ready():
	print ("ClassicBot is running")
	print ("Name: " + classicBot.user.name)
	print ("ID: " + classicBot.user.id)

@classicBot.event
async def on_message(message):
	channel = message.channel
	if((message.content.lower().find('fuck toan') >= 0) and (message.author.name != 'ClassicBot')):
		await classicBot.send_message(channel, 'No, Fuck you {}'.format(message.author.mention))
	await classicBot.process_commands(message)

@classicBot.command(pass_context=True)
async def info(ctx, user: discord.Member):
	embed = discord.Embed(title="{}'s Info".format(user.name), description="User info:", color=0x00ff00)
	embed.add_field(name="Name", value=user.name, inline=True)
	embed.add_field(name="ID", value=user.id, inline=True)
	embed.add_field(name="Status", value=user.status, inline=True)
	embed.add_field(name="Role", value=user.top_role, inline=True)
	embed.add_field(name="Joined", value=user.joined_at, inline=True)
	embed.set_thumbnail(url=user.avatar_url)
	await classicBot.say(embed=embed)

@classicBot.command(pass_context=True)
async def Momo(ctx):
	await classicBot.say("__**Momo is a bitch**__")

@classicBot.command(pass_context=True)
async def momo(ctx):
	await classicBot.say("__**Momo is a bitch**__")

@classicBot.command(pass_context=True)
async def Tulip(ctx):
	await classicBot.say("__**No.**__")

@classicBot.command(pass_context=True)
async def tulip(ctx):
	await classicBot.say("__**No.**__")

@classicBot.command(pass_context=True)
async def Gay(ctx, user: discord.Member):
	await classicBot.say("{} is ".format(user.mention) + "https://cdn.discordapp.com/emojis/482080671314083840.png?v=1")

@classicBot.command(pass_context=True)
@commands.has_role("Memes")
async def spam(ctx, user: discord.Member):
	await classicBot.say("{}".format(user.mention) + " WAKE UP")
	await classicBot.say("{}".format(user.mention) + " WAKE UP")
	await classicBot.say("{}".format(user.mention) + " WAKE UP")
	await classicBot.say("{}".format(user.mention) + " WAKE UP")
	await classicBot.say("{}".format(user.mention) + " WAKE UP")

@classicBot.command(pass_context=True)
@commands.has_role("Memes")
async def Spam(ctx, user: discord.Member):
	await classicBot.say("{}".format(user.mention) + " WAKE UP")
	await classicBot.say("{}".format(user.mention) + " WAKE UP")
	await classicBot.say("{}".format(user.mention) + " WAKE UP")
	await classicBot.say("{}".format(user.mention) + " WAKE UP")
	await classicBot.say("{}".format(user.mention) + " WAKE UP")

@classicBot.command(pass_context=True)
async def dice(ctx):
	dice = random.randint(1,6)
	await classicBot.say(dice)

@classicBot.command(pass_context=True)
async def m(ctx, input1=0, input2=0):
	result = input1*input2
	await classicBot.say(result)

@classicBot.command(pass_context=True)
async def d(ctx, input1=0, input2=0):
	result = input1/input2
	await classicBot.say(result)

@classicBot.command(pass_context=True)
async def a(ctx, input1=0, input2=0):
	result = input1+input2
	await classicBot.say(result)

@classicBot.command(pass_context=True)
async def s(ctx, input1=0, input2=0):
	result = input1-input2
	await classicBot.say(result)

@classicBot.command(pass_context=True)
async def bcoin(ctx, bcoins=0, rate=0):
	result = round((bcoins*(rate*.001)), 2)
	postfix = "Million"
	if(result >= 1000):
		result = round((result*.001), 4)
		postfix = "Billion"
		if(result >= 1000):
			result = round((result*.001), 6)
			postfix = "Trillion, you fucking whale"
	await classicBot.say(str(result) + " " + postfix)

@classicBot.command(pass_context=True)
@commands.has_permissions(manage_messages=True)
async def nuke(ctx, amount=5):
	channel = ctx.message.channel
	messages = []
	if (int(amount) >= 50):
		amount = 50
	async for message in classicBot.logs_from(channel, limit=int(amount)):
		messages.append(message)
	await classicBot.delete_messages(messages)
	await classicBot.say(str(amount) + " Messages Nuked :boom:")

@classicBot.command(pass_context=True)
async def profile(ctx, user: discord.Member):
	Level = 1
	lowExp = 0
	nextExp = 100
	await classicBot.say("```{} your stats are Level : ".format(user.name) + str(Level) + " Exp: " + str(lowExp) + "/" + str(nextExp) + "```")

@classicBot.command(pass_context=True)
async def Profile(ctx, user: discord.Member):
	Level = 55
	lowExp = 5141
	nextExp = 255000
	await classicBot.say("```{} your stats are Level : ".format(user.name) + str(Level) + " Exp: " + str(lowExp) + "/" + str(nextExp) + "```")






classicBot.loop.create_task(change_status())
classicBot.run(botKey)
