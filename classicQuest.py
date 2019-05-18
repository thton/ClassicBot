import pymysql.cursors
from dbsettings import *
import discord
from discord.ext import commands
from botKey import botKey

classicBot = commands.Bot(command_prefix='#')

connection = pymysql.connect(host=DB_HOST,
                             user=DB_USER,
                             password=DB_PASS,
                             db=DB_NAME,
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

print('Connected to %s' % DB_NAME)


class ClassicQuest:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self):
        await self.bot.say('Pong!')


def setup(bot):
    bot.add_cog(ClassicQuest(bot))


if __name__ == '__main__':
    setup(classicBot)
    classicBot.run(botKey)