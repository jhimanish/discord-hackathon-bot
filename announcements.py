import asyncio
from datetime import datetime
from discord.ext import tasks, commands
import discord
from pytz import timezone

# reading announcements file
announcements = []
with open("announcements.txt") as f:
    announcements = f.read().splitlines()


class Announcements(commands.Cog):
    def __init__(self, bot):
        self.index = 0
        self.printer.start()
        self.bot = bot

    def cog_unload(self):
        self.printer.cancel()

    @tasks.loop(seconds=60)
    async def printer(self):
        tz = timezone("EST")
        now = datetime.strftime(datetime.now(tz), "%A, %B %d %I %M %p")
        nowSplit = now.split()
        nowSplit[2] = str(int(nowSplit[2])) + "th"
        nowSplit[3] = str(int(nowSplit[3])) + ":" + nowSplit[4]
        channel = self.bot.get_channel(807666054058475520)  # CHANGE ID
        for i in announcements:
            j = i.split()
            if (
                j[0] == nowSplit[0]
                and j[1] == nowSplit[1]
                and j[2] == nowSplit[2]
                and j[3] == nowSplit[3]
                and j[4] == nowSplit[5]
            ):
                if channel != None:
                    role = discord.utils.get(
                        self.bot.get_guild(794312996314546196).roles, name="Hacker"
                    )
                    messages = "Hey " + role.mention + " " + " ".join(j[5:])
                    await channel.send(messages)


def setup(bot):
    bot.add_cog(Announcements(bot))
