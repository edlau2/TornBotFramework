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

    #########################################################

    @commands.command(name='repeat', aliases=['copy', 'mimic', 'echo'])
    async def do_repeat(self, ctx, *, our_input: str):

        #Your code will go here
        await ctx.send(our_input)

    #########################################################

    #@commands.command(name='help')
    #async def help(self, ctx):

        #Your code will go here
    #    await self.bot.say("Help me!")

    #########################################################

    @commands.command(name='embeds')
    async def example_embed(self, ctx):
        """A simple command which showcases the use of embeds.
        Have a play around and visit the Visualizer."""

        embed = discord.Embed(title='Example Embed',
                              description='Showcasing the use of Embeds...\nSee the visualizer for more info.',
                              colour=0x98FB98)
        embed.set_author(name='MysterialPy',
                         url='https://gist.github.com/MysterialPy/public',
                         icon_url='http://i.imgur.com/ko5A30P.png')
        embed.set_image(url='https://cdn.discordapp.com/attachments/84319995256905728/252292324967710721/embed.png')

        embed.add_field(name='Embed Visualizer', value='[Click Here!](https://leovoel.github.io/embed-visualizer/)')
        embed.add_field(name='Command Invoker', value=ctx.author.mention)
        embed.set_footer(text='Made in Python with discord.py@rewrite', icon_url='http://i.imgur.com/5BFecvA.png')

        await ctx.send(content='**A simple Embed for discord.py@rewrite in cogs.**', embed=embed)


def setup(bot):
       bot.add_cog(SimpleCog(bot))
