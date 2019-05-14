#Classic Bot
#Made by Toan Ton
#Version 0.0.2

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
statuses = ["Version 0.0.2", "Code forever", "Azur Lane"]

###############################################################################
#Basic bot functions
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

@classicBot.event
async def on_message(message):
	channel = message.channel
	if((message.content.lower().find('fuck toan') >= 0) and (message.author.name != 'ClassicBot')):
		await classicBot.send_message(channel, 'No, Fuck you {}'.format(message.author.mention))
	await classicBot.process_commands(message)

###############################################################################
#Music Bot functions
#Reference for music code: https://github.com/Rapptz/discord.py/blob/async/examples/playlist.py

class VoiceEntry:
	def __init__(self, message, player):
		self.requester = message.author
		self.channel = message.channel
		self.player = player

	def __str__(self):
		fmt = '*{0.title} uploaded by {0.uploader} and requested by {1.display_name}'
		duration = self.player.duration
		if duration:
			fmt = fmt + ' [length: {0[0]}m {0[1]}s]'.format(divmod(duration, 60))
		return fmt.format(self.player, self.requester)

class VoiceState:
	def __init__(self, bot):
		self.current = None
		self.voice = None
		self.bot = bot
		self.play_next_song = asyncio.Event()
		self.songs = asyncio.Queue()
		self.skip_votes = set() #set of user_ids that voted
		self.audio_player = self.bot.loop.create_task(self.audio_player_task())

	def is_playing(self):
		if self.voice is None or self.current is None:
			return False
		player = self.current.player
		return not player.is_done()

	@property
	def player(self):
		return self.current.player

	def skip(self):
		self.skip_votes.clear()
		if self.is_playing():
			self.player.stop()

	def toggle_next(self):
		self.bot.loop.call_soon_threadsafe(self.play_next_song.set)

	async def audio_player_task(self):
		while True:
			self.play_next_song.clear()
			self.current = await self.songs.get()
			await self.bot.send_message(self.current.channel, 'Now Playing ' + str(self.current))
			self.current.player.start()
			await self.play_next_song.wait()

class Music:
	def __init__(self, bot):
		self.bot = bot
		self.voice_states = {}

	def get_voice_state(self, server):
		state = self.voice_states.get(server.id)
		if state is None:
			state = VoiceState(self.bot)
			self.voice_states[server.id] = state
		return state

	async def create_voice_client(self, channel):
		voice = await self.bot.join_voice_channel(channel)
		state = self.get_voice_state(channel.server)
		state.voice = voice

	def __unload(self):
		for state in self.voice_states.value():
			try:
				state.audio_player.cancel()
				if state.voice():
					self.bot.loop.create_task(state.voice.disconnect())
			except:
				pass

	@commands.command(pass_context=True, no_pm=True)
	async def join(self, ctx, *, channel : discord.Channel):
		try:
			await self.create_voice_client(channel)
		except discord.ClientException:
			await self.bot.say('Already in a voice channel...')
		except discord.InvalidArgument:
			await self.bot.say('This is not a voice channel...')
		else:
			await self.bot.say('Ready to play audio in ' + channel.name)

	@commands.command(pass_context=True, no_pm=True)
	async def summon(self, ctx):
		summoned_channel = ctx.message.author.voice_channel
		if summoned_channel is None:
			await self.bot.say('You are not in a voice channel.')
			return False
		state = self.get_voice_state(ctx.message.server)
		if state.voice is None:
			state.voice = await self.bot.join_voice_channel(summoned_channel)
		else:
			await state.voice.move_to(summoned_channel)
		return True

	@commands.command(pass_context=True, no_pm=True)
	async def play(self, ctx, *, song : str):
		state = self.get_voice_state(ctx.message.server)
		opts = {
			'default_search': 'auto',
			'quiet': True,
		}
		beforeArgs = "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"
		if state.voice is None:
			success = await ctx.invoke(self.summon)
			if not success:
				return
		try:
			player = await state.voice.create_ytdl_player(song, before_options=beforeArgs, ytdl_options=opts, after=state.toggle_next)
		except Exception as e:
			fmt = 'An error occurred while processing this request: ```py\n{}: {}\n```'
			await self.bot.send_message(ctx.message.channel, fmt.format(type(e).__name__,e))
		else:
			player.volume = 0.6
			entry = VoiceEntry(ctx.message, player)
			await self.bot.say('Enqueued ' + str(entry))
			await state.songs.put(entry)

	@commands.command(pass_context=True, no_pm=True)
	async def volume(self, ctx, value : int):
		state = self.get_voice_state(ctx.message.server)
		if state.is_playing():
			player = state.player
			player.volume = value / 100
			await self.bot.say('Set the volume to {:.0%}'.format(player.volume))

	@commands.command(pass_context=True, no_pm=True)
	async def pause(self, ctx):
		state = self.get_voice_state(ctx.message.server)
		if state.is_playing():
			player = state.player
			player.pause()

	@commands.command(pass_context=True, no_pm=True)
	async def resume(self, ctx):
		state = self.get_voice_state(ctx.message.server)
		if state.is_playing():
			player = state.player
			player.resume()

	@commands.command(pass_context=True, no_pm=True)
	async def stop(self, ctx):
		server = ctx.message.server
		state = self.get_voice_state(server)
		if state.is_playing():
			player = state.player
			player.stop()
		try:
			state.audio_player.cancel()
			del self.voice_states[server.id]
			await state.voice.disconnect()
		except:
			pass

	@commands.command(pass_context=True, no_pm=True)
	async def skip(self, ctx):
		state = self.get_voice_state(ctx.message.server)
		if not state.is_playing():
			await self.bot.say('Not playing any music right now...')
			return
		voter = ctx.message.author
		if voter == state.current.requester:
			await self.bot.say('Requester requested skipping song...')
			state.skip()
		elif voter.id not in state.skip_votes:
			state.skip_votes.add(voter.id)
			total_votes = len(state.skip_votes)
			if total_votes >= 3:
				await self.bot.say('Skip vote passed, skipping song...')
				state.skip()
			else:
				await self.bot.say('Skip vote added, currently at [{}/3]'.format(total_votes))
		else:
			await self.bot.say('You have already voted to skip this song.')

	@commands.command(pass_context=True, no_pm=True)
	async def playing(self, ctx):
		state = self.get_voice_state(ctx.message.server)
		if state.current is None:
			await self.bot.say('Not playing anything.')
		else:
			skip_count = len(state.skip_votes)
			await self.bot.say('Now playing {} [skips: {}/3]'.format(state.current, skip_count))

###############################################################################

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

###############################################################################
#Starting up the bot
classicBot.add_cog(Music(classicBot))
classicBot.loop.create_task(change_status())
classicBot.run(botKey)
