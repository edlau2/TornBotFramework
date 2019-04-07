#
# TornBotFramework.py
# A class driven, generic framework to which any command may easily be added.
# To add a new command, simply add the function in the section that has a comment
# that says: "This section is where any new commands can be added"
#
# After adding the function, be sure to register it with the command handler, 
# using the class's add_command() function. That's it. Easy peasy, lemon squeezy.
#
import discord
import requests
import json
import os
import sys
import random
import threading

from discord.ext import commands    # Extension handling module

import config                       # Private config file, contains our token

###############################################################################
#
# Command handler class
# Performs the execution of entered commands.
#
###############################################################################

class CommandHandler:

    # constructor
    def __init__(self, bot):
        self.bot = bot
        self.commands = []

    # Adds a command to our list of known commands
    def add_command(self, command):
        self.commands.append(command)

###############################################################################
#
# Extension (cog) manager class
# used to keep track of loaded, unloaded, and available extensions
#
###############################################################################

class ExtensionManager:

    # constructor
    def __init__(self, bot):
        self.bot = bot
        self.loaded_extensions = []
        self.all_extensions = []

    # Loads an extension and add to our lists of known and loaded extensions
    def load_local_extension(self, extension):
        self.all_extensions.append(extension)
        try:
            self.bot.load_extension('cogs.{}'.format(extension))
            print('Loaded extension {}'.format(extension))
        except Exception as e:
            print('Failed to load extension {}: {}'.format(extension, e))
            return
        self.loaded_extensions.append(extension)

    # Unloads (stops) an extension and remove from our list of loaded extensions
    def unload_local_extension(self, extension):
        try:
            self.bot.unload_extension('cogs.{}'.format(extension))
            print('Unloaded extension {}'.format(extension))
        except Exception as e:
            print('Failed to unload extension {}: {}'.format(extension, e))
            return
        self.loaded_extensions.remove(extension)

    # Reloads an extension, or load if not already loaded
    def reload_local_extension(self, extension):
        if extension in self.loaded_extensions:
            self.bot.reload_extension('cogs.{}'.format(extension))
            return 'Extension {} reloaded'.format(extension)
        # not loaded, so just load.
        self.load_local_extension(all_extensions)

    # Lists loaded extensions
    def list_loaded_extensions(self):
        count = 0
        ret = "**Loaded Extensions:**\n"
        for extension in self.loaded_extensions:
            ret += '{}\n'.format(extension)
            count += 1
        if (count == 0):
            ret += '<none>'
        return ret

    # Lists all known extensions
    def list_all_extensions(self):
        ret = "**All known Extensions:**\n"
        for extension in self.all_extensions:
            ret += '{}\n'.format(extension)
        return ret

    def get_extension_commands(self):
        return '\n<Help for all loaded extensions not yet implemented>'

    
###############################################################################
#
# Create the discord bot, command handler, and extension manager 
#
################################################################################

bot = commands.Bot(command_prefix=config.BOT_CONFIG['prefix'], description='Icarus')
ch = CommandHandler(bot)
xm = ExtensionManager(bot)

###############################################################################
#
# This section is where any new commands can be added. Can do anything you
# want, just be sure to add to the command handler so it gets executed.
#
# I've followed the convention of inserting this immediately after the
# function itself, see below
#
# ch.add_command({
#    'trigger': '!<name of command>',
#    'function': <name of the function>,
#    'args_num': <number of arrguments the command expects>,
#    'args_name': <name of arguments>,
#    'description': <obvious>
# }) 
#
###############################################################################

##
## Start of the !help command
## Simply lists commands accepted
##
#@bot.command(name='help', aliases=['!h', '!?'])
#async def commands_command(message, bot, args):
#    try:
#        coms = '**Native Command List**\n'
#        count = 0
#        for command in ch.commands:
#            if (command == '!kill'):
#                continue
#            count += 1
#            aliases = ', '.join(command['aliases'])
#            if not aliases:
#                coms += '{}.) {}: {}\n'.format(count, command['trigger'], command['description'])
#            else:
#                coms += '{}.) {} or {}: {}\n'.format(count, command['trigger'], aliases, command['description'])

        # Now iterate loaded extensions and see if they support !help
#        coms += '\n**Loaded Extensions Command List**'
#        coms += xm.get_extension_commands()
#        return coms
#    except Exception as e:
#        print(e)

#ch.add_command({
#    'trigger': '!help',
#    'aliases': ['!h', '!?'],
#    'function': commands_command,
#    'args_num': 0,
#    'args_name': [],
#    'description': 'Prints a list of all the commands!'
#})
## end help command

##
## Start of the !Hello comnmand. Just says "Hello" to whatever is args[0]
##
@bot.command(name='hello')
async def hello_function(message,bot,args):
    try:
        return '{}, {} says Hello!'.format(args[0], message.author)
    except Exception as e:
        return e

ch.add_command({
    'trigger': '!hello',
    'aliases': "",
    'function': hello_function,
    'args_num': 1,
    'args_name': ['string'],
    'description': 'Will say hello to args[0] from the caller'
})
#end hello command

##
## Start of the !ip command. This is an example of using
## HTTP, which will be usefull for interacting with the Torn API
##
@bot.command(pass_context=True, name='ip')
async def ip_command(ctx, args):
    try:
        req = requests.get('http://ip-api.com/json/{}'.format(args[0]))
        resp = json.loads(req.content.decode())
        if req.status_code == 200:
            if resp['status'] == 'success':
                template = '**{}**\n**IP: **{}\n**City: **{}\n**State: **{}\n**Country: **{}\n**Latitude: **{}\n**Longitude: **{}\n**ISP: **{}'
                out = template.format(args[0], resp['query'], resp['city'], resp['regionName'], resp['country'], resp['lat'], resp['lon'], resp['isp'])
                return out
            elif resp['status'] == 'fail':
                return 'API Request Failed'
        else:
            return 'HTTP Request Failed: Error {}'.format(req.status_code)
    except Exception as e:
        print(e)

ch.add_command({
    'trigger': '!ip',
    'aliases': "",
    'function': ip_command,
    'args_num': 1,
    'args_name': ['IP\Domain'],
    'description': 'Prints information about provided IP/Domain'
})
## end ip command

###################################   TESTING #################################################
@bot.command(pass_context=True, name='shuffle')
async def shuffle_function(ctx, args):
    l = list(args)
    random.shuffle(l)
    await bot.say("Shuffled: '" + args + "' got '" + (''.join(str(e) for e in l) + "'"))

@bot.command(pass_context=True, name='test') 
async def test_function(ctx): 
    #item = self.random_item()
    item = "Wolverine Plushie"
    parts = item.split(' ')
    shuffled = ''
    for x in parts:
        c = list(x)
        random.shuffle(c)
        shuffled = shuffled + " " + (''.join(str(e) for e in c))

    print("Original: " + item) 
    print("Shuffled: " + shuffled)
        
    await bot.say("Original: " + "||" + item + "||") 
    await bot.say("Shuffled: " + shuffled.lower())

@bot.command(pass_context=True, name='test2') 
async def test2_function(ctx):
       percent = 30
       scramword = "some test string I made up"
       r = '' 
       await bot.say("Test String (scramword): " + scramword) 
       for x in scramword: 
            if x == ' ': 
                r += str(x)
                continue
            if random.randint(0, 100) <= percent: 
                r += str(x) 
            else: 
                r += '*' 

           # r+= (random.int(100) <= percent) ? x : '*'
            
       await bot.say("Output: ```" + r + '```');
       return r

# testing function

# Wrapper for tim-out fn.
def wrapper() :
    timed_out()

#global timer
t = threading.Timer(5.0, wrapper)


def timed_out(args):
    print("Timer timed out!")
    print(bot)
    #await bot.say("Test3: timed out!")
    t.cancel()
    # reset - is this needed?
    t = threading.Timer(5.0, timed_out)

#global timer
#t = threading.Timer(5.0, timed_out)

# Command to test cancellables with
@bot.command(pass_context=True, name='test3') 
async def test3_function(ctx):
    await bot.say("Started Test3, '!cancel' aborts, otherwise in 30 seconds you die.")
    t = threading.Timer(5.0, timed_out, [bot])
    t.start()
    await bot.say("timer started...")

#command to cancel, in RL, call from message handler
@bot.command(pass_context=True, name='cancel') 
async def cancel_function(ctx):
    await bot.say("Cancelling timer....")
    t.cancel()
    # reset - is this needed?
    t = threading.Timer(5.0, timed_out)
    await bot.say("Cancelled..")

################################### END TESTING ###############################################

# This command *should* stop the bot. Not sure I want this to be in !help, or even here at all.
@bot.command(name='kill', aliases=['k'])
async def kill_function(message,bot,args):
    bot.send_message(message.channel, 'Killing Icarus. Bye!')
    #bot.close()

ch.add_command({
    'trigger': '!kill',
    'aliases': ['!k'],
    'function': kill_function,
    'args_num': 0,
    'args_name': ['string'],
    'description': 'Kills the bot.'
})             

###############################################################################
#
# Cog (extension) handling functions
#
###############################################################################

##
## Start of the !scog command, stops (unloads) a cog
##
@bot.command(name='scog', aliases=['stop', 'unload'])
async def scog_function(message,bot,args):
    try:
        ret = '{} is stopping extension {}'.format(message.author, args[0])
        xm.unload_local_extension(args[0])
        ret += '\n{} stopped.'.format(args[0])
        return ret
    except Exception as e:
        return e

ch.add_command({
    'trigger': '!scog',
    'aliases': ['!stop', '!unload'],
    'function': scog_function,
    'args_num': 1,
    'args_name': ['string'],
    'description': 'Will stop the extension with the provided name'
})
#end !scog command

##
## Start of the !rcog command, reloads a cog
## [p]reload mycog
##
@bot.command(name='rcog', aliases=['load', 'reload'])
async def rcog_function(message,bot,args):
    try:
        ret = '{} is stopping extension {}'.format(message.author, args[0])
        xm.reload_local_extension(args[0])
        ret += '\n{} reloaded.'.format(args[0])
        return ret
    except Exception as e:
        return e

ch.add_command({
    'trigger': '!rcog',
    'aliases': ['!load', '!reload'],
    'function': rcog_function,
    'args_num': 1,
    'args_name': ['string'],
    'description': 'Will reload the extension with the provided name'
})
#end !rcog command

##
## Start of the !llcog command, lists loaded cogs
##
@bot.command(name='llcog', aliases=['loaded', 'loadedcogs'])
async def llcog_function(message,bot,args):
    try:
        return xm.list_loaded_extensions()
    except Exception as e:
        return e

ch.add_command({
    'trigger': '!llcog',
    'aliases': ['!loaded', '!loadedcogs'],
    'function': llcog_function,
    'args_num': 0,
    'args_name': ['string'],
    'description': 'Will list all loaded extensions'
})
#end !llcog command

##
## Start of the !lcog command, lists all known cogs
##
@bot.command(name='lcog', aliases=['known', 'knowncogs'])
async def lcog_function(message,bot,args):
    try:
         return xm.list_all_extensions()
    except Exception as e:
        return e

ch.add_command({
    'trigger': '!lcog',
    'aliases': ['!known', '!knowncogs'],
    'function': lcog_function,
    'args_num': 0,
    'args_name': ['string'],
    'description': 'Will list all known extensions'
})
#end !lcog command

###############################################################################
#
# bot is ready! This is where messages are processed and routed to the correct 
# command handler code.
#
###############################################################################
@bot.event
async def on_ready():
    try:
        print('Using discord.py version {}'.format(discord.__version__))
        print('Python version: {}'.format(sys.version))
        print('User name: {}'.format(bot.user.name))
        print('User ID: {}'.format(bot.user.id))
    except Exception as e:
        print(e)


if __name__ == '__main__':
    # Debugging
    print('Current working directory: {}'.format(os.getcwd()))

    # Load all found cogs
    for extension in os.listdir("cogs"):
        if extension.endswith(".py"):         
             xm.load_local_extension(extension[:-3])

#
# Start the bot!
#
# Note: the token is stored in a file called config.py
#
bot.run(config.BOT_CONFIG['token'])
