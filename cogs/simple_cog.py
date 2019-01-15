#
# This is the basic boiler plate for building a cog.
# It goes into the "cogs" subdirectry.
#
import discord
from discord.ext import commands

class SimpleCog:
    """Boilerplate for a simple cog"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def simple(self):     # This is the name of the command, "simple" in this case

        #Your code will go here
        await self.bot.say("Hello, I am a simple cog!")

def setup(bot):
    bot.add_cog(SimpleCog(bot))
