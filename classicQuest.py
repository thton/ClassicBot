import pymysql.cursors
from dbsettings import *
import discord
from discord.ext import commands
from botKey import botKey

classicBot = commands.Bot(command_prefix='#')


def connect_database():
    connection = pymysql.connect(host=DB_HOST,
                                 user=DB_USER,
                                 password=DB_PASS,
                                 db=DB_NAME,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

    print('Connected to database %s' % DB_NAME)
    return connection


class ClassicQuest:

    def __init__(self, bot):
        self.db = connect_database()
        self.bot = bot
        self.start()

    @commands.command()
    async def ping(self):
        await self.bot.say('Pong!')

    def get_user(self, user_id):
        try:
            with self.db.cursor() as cursor:
                sql = "SELECT * FROM `users` WHERE `user_id`=%s"
                cursor.execute(sql, user_id)
                result = cursor.fetchone()
                if not result:
                    print("User does not exist: %s" % user_id)
                else:
                    return result
        except Exception as e:
            print("Error looking up user id %s.\n%s" % (user_id, e))

    def add_all_users_to_db(self):
        for member in self.bot.get_all_members():
            self.add_user_to_db(member)

    def add_user_to_db(self, member):
        if self.get_user(member.id):
            return

        try:
            with self.db.cursor() as cursor:
                sql = "INSERT INTO `users` (`user_id`, `exp`, `coins`) VALUES (%s, %s, %s)"
                cursor.execute(sql, (member.id, 0, 0))
                self.db.commit()
                print("Added user %s to database." % member.id)
        except Exception as e:
            print("Error adding a user: %s" %e)

    def update_exp_points(self, member, points):
        user_info = self.get_user(member.id)
        with self.db.cursor() as cursor:
            try:
                sql = "UPDATE `users` SET `exp`=%s WHERE `user_id`=%s"
                new_exp_value = user_info['exp'] + points
                cursor.execute(sql, (new_exp_value, member.id))
                self.db.commit()
                print("Updated user %s experience points from %s to %s." %
                      (member.name, user_info['exp'], new_exp_value))
            except Exception as e:
                print("Error while updating xp points for %s; %s" % (member.id, e))

    def start(self):

        @self.bot.event
        async def on_ready():
            self.add_all_users_to_db()
            print("ClassicBot is running")
            print("Name: " + classicBot.user.name)
            print("ID: " + classicBot.user.id)

        @self.bot.event
        async def on_member_join(member):
            self.add_user_to_db(member)

        @self.bot.event
        async def on_message(message):
            self.update_exp_points(message.author, 1)
            if (message.content.lower().find('fuck toan') >= 0) and (message.author.name != 'ClassicBot'):
                await self.bot.send_message(message.channel, 'No, Fuck you {}'.format(message.author.mention))
            await self.bot.process_commands(message)

        @self.bot.command(name='profile',
                          aliases=['stats'],
                          pass_context=True)
        async def profile(ctx):
            user = self.get_user(ctx.message.author.id)
            await self.bot.say("Stats for %s Exp: %s Coins: %s" % (ctx.message.author.mention, user['exp'], user['coins']))


def setup(bot):
    bot.add_cog(ClassicQuest(bot))


if __name__ == '__main__':
    setup(classicBot)
    classicBot.run(botKey)