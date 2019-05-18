# Classic Bot
# Made by Toan Ton
# Version 0.0.2

import discord
from discord.ext import commands
import asyncio
from itertools import cycle
import random
from botKey import botKey

classicBot = commands.Bot(command_prefix='#')
classicBot.remove_command("help")
statuses = ["Version 0.0.2", "Code forever", "Azur Lane"]
extensions = ['classicMusic', 'classicQuest']


###############################################################################
# Basic bot functions
# change status every 60 seconds
async def change_status():
    await classicBot.wait_until_ready()
    status = cycle(statuses)
    while not classicBot.is_closed:
        current_status = next(status)
        await classicBot.change_presence(game=discord.Game(name=current_status))
        await asyncio.sleep(60)


# prints in console when bot is running and ready
@classicBot.event
async def on_ready():
    print("ClassicBot is running")
    print("Name: " + classicBot.user.name)
    print("ID: " + classicBot.user.id)


@classicBot.command(pass_context=True)
async def help(ctx):
    author = ctx.message.author

    helpmessage = discord.Embed(
        colour=discord.Colour.green()
    )

    helpmessage.set_author(name="Help")
    helpmessage.add_field(name="#info", value="([@Someone]) Returns info about the mentioned user", inline=False)
    helpmessage.add_field(name="#momo", value="Returns a Momo specific message", inline=False)
    helpmessage.add_field(name="#tulip", value="Returns a Tulip specific message", inline=False)
    helpmessage.add_field(name="#Gay",
                          value="([@Someone]) Returns a message calling the mentioned user gay with an image",
                          inline=False)
    helpmessage.add_field(name="#spam",
                          value="([@Someone]) Makes the bot spam the mentioned user 5 times, must have the Memes role",
                          inline=False)
    helpmessage.add_field(name="#dice", value="Rolls a dice between 1 and 6", inline=False)
    helpmessage.add_field(name="#m | #d | #a | #s",
                          value="([number] [number]) Basic multiply, divide, add, and subtract commands", inline=False)
    helpmessage.add_field(name="#bcoin",
                          value="([bcoins] [rate]) Burning Soulworker specific command for selling Bcoin", inline=False)
    helpmessage.add_field(name="#nuke",
                          value='([number of messages to delete]) Used for mass deletion of messages, caps at 50, and must have delete powers',
                          inline=False)

    await classicBot.send_message(author, embed=helpmessage)


@classicBot.event
async def on_message(message):
    channel = message.channel
    if (message.content.lower().find('fuck toan') >= 0) and (message.author.name != 'ClassicBot'):
        await classicBot.send_message(channel, 'No, Fuck you {}'.format(message.author.mention))
    await classicBot.process_commands(message)


###############################################################################
# Main standalone bot commands

@classicBot.command(pass_context=True)
async def info(user: discord.Member):
    embed = discord.Embed(title="{}'s Info".format(user.name), description="User info:", color=0x00ff00)
    embed.add_field(name="Name", value=user.name, inline=True)
    embed.add_field(name="ID", value=user.id, inline=True)
    embed.add_field(name="Status", value=user.status, inline=True)
    embed.add_field(name="Role", value=user.top_role, inline=True)
    embed.add_field(name="Joined", value=user.joined_at, inline=True)
    embed.set_thumbnail(url=user.avatar_url)
    await classicBot.say(embed=embed)


@classicBot.command(pass_context=True)
async def momo():
    await classicBot.say("__**Momo is a bitch**__")


@classicBot.command(pass_context=True)
async def tulip():
    await classicBot.say("__**No.**__")


@classicBot.command(pass_context=True)
async def gay(user: discord.Member):
    await classicBot.say("{} is ".format(user.mention) + "https://cdn.discordapp.com/emojis/482080671314083840.png?v=1")


@classicBot.command(pass_context=True)
@commands.has_role("Memes")
async def spam(user: discord.Member):
    await classicBot.say("{}".format(user.mention) + " WAKE UP")
    await classicBot.say("{}".format(user.mention) + " WAKE UP")
    await classicBot.say("{}".format(user.mention) + " WAKE UP")
    await classicBot.say("{}".format(user.mention) + " WAKE UP")
    await classicBot.say("{}".format(user.mention) + " WAKE UP")


@classicBot.command(pass_context=True)
async def dice():
    result = random.randint(1, 6)
    await classicBot.say(result)


@classicBot.command(pass_context=True)
async def m(input1=0, input2=0):
    result = input1 * input2
    await classicBot.say(result)


@classicBot.command(pass_context=True)
async def d(input1=0, input2=0):
    result = input1 / input2
    await classicBot.say(result)


@classicBot.command(pass_context=True)
async def a(input1=0, input2=0):
    result = input1 + input2
    await classicBot.say(result)


@classicBot.command(pass_context=True)
async def s(input1=0, input2=0):
    result = input1 - input2
    await classicBot.say(result)


@classicBot.command(pass_context=True)
async def bcoin(bcoins=0, rate=0):
    result = round((bcoins * (rate * .001)), 2)
    postfix = "Million"
    if result >= 1000:
        result = round((result * .001), 4)
        postfix = "Billion"
        if result >= 1000:
            result = round((result * .001), 6)
            postfix = "Trillion, you fucking whale"
    await classicBot.say(str(result) + " " + postfix)


@classicBot.command(pass_context=True)
@commands.has_permissions(manage_messages=True)
async def nuke(ctx, amount=5):
    channel = ctx.message.channel
    messages = []
    if int(amount) >= 50:
        amount = 50
    async for message in classicBot.logs_from(channel, limit=int(amount)):
        messages.append(message)
    await classicBot.delete_messages(messages)
    await classicBot.say(str(amount) + " Messages Nuked :boom:")


@classicBot.command(pass_context=True)
async def test(user: discord.Member):
    level = 1
    lowexp = 0
    nextexp = 100
    await classicBot.say(
        "```{} your stats are Level : ".format(user.name) + str(level) + " Exp: " + str(lowexp) + "/" + str(
            nextexp) + "```")

###############################################################################
# Starting up the bot
if __name__ == '__main__':
    for extension in extensions:
        try:
            classicBot.load_extension(extension)
        except Exception as e:
            print('Error loading extensions %s' % e)
    classicBot.loop.create_task(change_status())
    classicBot.run(botKey)
