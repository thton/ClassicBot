#Classic Bot
#Made by Toan Ton
#Version 0.0.1

import discord
from discord.ext import commands
from discord.ext.commands import Bot
import youtube_dl
import asyncio
from itertools import cycle
import random

with open('botKey.txt', 'r') as key:
	botKey = key.readline()

classicBot = commands.Bot(command_prefix='#')
classicBot.remove_command("help")
statuses = ["Version 0.0.1", "Code forever", "Azur Lane"]

#music player variables
players = {}
queues = {}
#change status every 60 seconds
async def change_status():
	await classicBot.wait_until_ready()
	status = cycle(statuses)
	while not classicBot.is_closed:
		current_status = next(status)
		await classicBot.change_presence(game=discord.Game(name=current_status))
		await asyncio.sleep(60)
#prints in console when bot is running and ready
@classicBot.event
async def on_ready():
	print ("ClassicBot is running")
	print ("Name: " + classicBot.user.name)
	print ("ID: " + classicBot.user.id)

@classicBot.command(pass_context=True)
async def help(ctx):
	author = ctx.message.author

	helpmessage = discord.Embed(
		colour = discord.Colour.green()
	)

	helpmessage.set_author(name="Help")
	helpmessage.add_field(name="#info", value="([@Someone]) Returns info about the mentioned user", inline=False)
	helpmessage.add_field(name="#momo", value="Returns a Momo specific message", inline=False)
	helpmessage.add_field(name="#tulip", value="Returns a Tulip specific message", inline=False)
	helpmessage.add_field(name="#Gay", value="([@Someone]) Returns a message calling the mentioned user gay with an image", inline=False)
	helpmessage.add_field(name="#spam", value="([@Someone]) Makes the bot spam the mentioned user 5 times, must have the Memes role", inline=False)
	helpmessage.add_field(name="#dice", value="Rolls a dice between 1 and 6", inline=False)
	helpmessage.add_field(name="#m | #d | #a | #s", value="([number] [number]) Basic multiply, divide, add, and subtract commands", inline=False)
	helpmessage.add_field(name="#bcoin", value="([bcoins] [rate]) Burning Soulworker specific command for selling Bcoin", inline=False)
	helpmessage.add_field(name="#nuke", value="([number of messages to delete]) Used for mass deletion of messages, caps at 50, and must have delete powers", inline=False)

	await classicBot.send_message(author, embed=helpmessage)

@classicBot.command(pass_context=True)
async def join(ctx):
	channel = ctx.message.author.voice.voice_channel
	await classicBot.join_voice_channel(channel)

@classicBot.command(pass_context=True)
async def leave(ctx):
	server = ctx.message.server
	voice_client = classicBot.voice_client_in(server)
	await voice_client.disconnect()

@classicBot.event
async def on_message(message):
	channel = message.channel
	if((message.content.lower().find('fuck toan') >= 0) and (message.author.name != 'ClassicBot')):
		await classicBot.send_message(channel, 'No, Fuck you {}'.format(message.author.mention))
	await classicBot.process_commands(message)

def check_queue(id):
	if queues[id] != []:
		player = queues[id].pop(0)
		players[id] = player
		player.start()

@classicBot.command(pass_context=True)
async def play(ctx, url):
	server = ctx.message.server
	voice_client = classicBot.voice_client_in(server)
	beforeArgs = "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"
	player = await voice_client.create_ytdl_player(url, before_options=beforeArgs, after=lambda: check_queue(server.id))
	if server.id in queues:
		queues[server.id].append(player)
		await classicBot.say("Video queued")
	else:
		players[server.id] = player
		player.start()

@classicBot.command(pass_context=True)
async def queue(ctx, url):
	server = ctx.message.server
	voice_client = classicBot.voice_client_in(server)
	beforeArgs = "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"
	player = await voice_client.create_ytdl_player(url, before_options=beforeArgs, after=lambda: check_queue(server.id))

	if server.id in queues:
		queues[server.id].append(player)
	else:
		queues[server.id] = [player]
	await classicBot.say("Video queued")

@classicBot.command(pass_context=True)
async def volume(ctx, volume: int):
	id = ctx.message.server.id
	players[id].volume = .1*double(volume)

@classicBot.command(pass_context=True)
async def pause(ctx):
	id = ctx.message.server.id
	players[id].pause()

@classicBot.command(pass_context=True)
async def stop(ctx):
	id = ctx.message.server.id
	players[id].stop()
	server = ctx.message.server
	queues = {}
	voice_client = classicBot.voice_client_in(server)
	await voice_client.disconnect()

@classicBot.command(pass_context=True)
async def skip(ctx):
	id = ctx.message.server.id
	players[id].stop()

@classicBot.command(pass_context=True)
async def resume(ctx):
	id = ctx.message.server.id
	players[id].resume()

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
