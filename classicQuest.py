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


def get_required_exp(level):
    exp_required = (level+1)*(level+1)*100
    return exp_required


class ClassicQuest:

    def __init__(self, bot):
        self.db = connect_database()
        self.bot = bot
        self.start()

    @commands.command()
    async def ping(self):
        await self.bot.say('Pong!')

    @commands.command(name='profile',
                      aliases=['stats'],
                      pass_context=True)
    async def profile(self, ctx):
        user = self.get_user(ctx.message.author.id)
        profile = discord.Embed(
            colour=discord.Colour.dark_green()
        )
        profile.set_author(name="Profile for %s" % ctx.message.author.name)
        profile.add_field(name="Level", value=user['level'], inline=False)
        profile.add_field(name="Exp", value="%s/%s" % (user['exp'], get_required_exp(user['level'])), inline=False)
        profile.add_field(name="Coins :moneybag:", value=user['coins'], inline=False)
        await self.bot.say(embed=profile)

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
                sql = "INSERT INTO `users` (`user_id`, `exp`, `coins`, `level`) VALUES (%s, %s, %s, %s)"
                cursor.execute(sql, (member.id, 0, 0, 0))
                self.db.commit()
                print("Added user %s to database." % member.id)
        except Exception as e:
            print("Error adding a user: %s" %e)

    def update_exp_points(self, member, points):
        user_info = self.get_user(member.id)
        needed_exp_to_level = get_required_exp(user_info['level'])
        with self.db.cursor() as cursor:
            try:
                sql = "UPDATE `users` SET `exp`=%s WHERE `user_id`=%s"
                new_exp_value = user_info['exp'] + points
                cursor.execute(sql, (new_exp_value, member.id))
                self.db.commit()
                print("Updated user %s experience points from %s to %s." %
                      (member.name, user_info['exp'], new_exp_value))
                print("Needed exp to level: %s" % needed_exp_to_level)
                if new_exp_value >= needed_exp_to_level:    # level up if exp required is hit
                    self.level_up(member, user_info, needed_exp_to_level)
            except Exception as e:
                print("Error while updating exp points for %s; %s" % (member.id, e))

    def level_up(self, member, user_info, used_exp):
        with self.db.cursor() as cursor:
            try:
                sql = "UPDATE `users` SET `level`=%s WHERE `user_id`=%s"
                new_level = user_info['level'] + 1
                cursor.execute(sql, (new_level, member.id))
                self.db.commit()
                print("%s leveled up and is now level %s" % (member.name, new_level))
                self.update_exp_points(member, (-1 * used_exp))
            except Exception as e:
                print("Error while updating player level for %s; %s" % (member.name, e))

    def start(self):

        @self.bot.event     # overrides on_ready in MainBot
        async def on_ready():
            self.add_all_users_to_db()
            print("ClassicBot is running")
            print("Name: " + self.bot.user.name)
            print("ID: " + self.bot.user.id)

        @self.bot.event
        async def on_member_join(member):
            self.add_user_to_db(member)

        @self.bot.event     # overrides on_message in MainBot
        async def on_message(message):
            self.update_exp_points(message.author, 1)
            if (message.content.lower().find('fuck toan') >= 0) and (message.author.name != 'ClassicBot'):
                await self.bot.send_message(message.channel, 'No, Fuck you {}'.format(message.author.mention))
            await self.bot.process_commands(message)


def setup(bot):
    bot.add_cog(ClassicQuest(bot))


if __name__ == '__main__':
    setup(classicBot)
    classicBot.run(botKey)